"""
Evals - An LLM-as-a-judge evaluation tool
"""

import os
import json
import logging
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Optional, Any, Union, Tuple
import openai
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables if .env exists
load_dotenv()

class EvaluationResult(BaseModel):
    """Result of an LLM evaluation."""
    query: str
    response: str
    reference: Optional[str] = None
    scores: Dict[str, float] = Field(default_factory=dict)
    reasoning: Dict[str, str] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    
    def overall_score(self) -> float:
        """Calculate the weighted average score across all criteria."""
        if not self.scores:
            return 0.0
        weights = self.metadata.get('criteria_weights', {})
        total_weight = sum(weights.values()) or len(self.scores)
        weighted_sum = sum(score * weights.get(criterion, 1.0) 
                         for criterion, score in self.scores.items())
        return weighted_sum / total_weight

class Evals:
    """Simple LLM-as-a-judge evaluation tool."""
    
    def __init__(
        self,
        model: str = "gpt-4o",
        criteria: Optional[Dict[str, str]] = None,
        criteria_weights: Optional[Dict[str, float]] = None,
        scale: int = 5,
        temperature: float = 0.0,
        api_key: Optional[str] = None,
        enable_logging: bool = True,
    ):
        """
        Initialize the evaluator.
        
        Args:
            model: The LLM model to use (default: gpt-4o)
            criteria: Dictionary of criteria names to descriptions
            criteria_weights: Optional weights for each criterion
            scale: Evaluation scale (default: 1-5)
            temperature: Model temperature
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
            enable_logging: Whether to enable detailed logging
        """
        self.model = model
        self.scale = scale
        self.temperature = temperature
        self.enable_logging = enable_logging
        
        # Set up OpenAI client
        api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("No API key provided. Set OPENAI_API_KEY environment variable or pass api_key to Evals.")
        self.client = openai.OpenAI(api_key=api_key)
        
        # Default criteria if none provided
        self.criteria = criteria or {
            "accuracy": "Is the information accurate and factual?",
            "completeness": "Does the response address all aspects of the query?",
            "helpfulness": "Is the response helpful to the user?",
            "clarity": "Is the response clear and well-structured?",
            "originality": "Does the response demonstrate original thinking?"
        }
        
        # Set default weights if none provided
        self.criteria_weights = criteria_weights or {
            criterion: 1.0 for criterion in self.criteria
        }
        
        if enable_logging:
            logger.info(f"Initialized LLMQualityAssessor with model: {model}")
            logger.info(f"Using criteria: {list(self.criteria.keys())}")
    
    def _build_prompt(self, query: str, response: str, reference: Optional[str] = None) -> str:
        """Build the evaluation prompt."""
        prompt = f"""You are an impartial judge evaluating the quality of an AI assistant's response to a user query.
        
User Query: "{query}"

AI Response: "{response}"
"""
        
        if reference:
            prompt += f'\nReference Answer: "{reference}"\n'
        
        prompt += "\nEvaluate the AI response using the following criteria:\n"
        
        for criterion, description in self.criteria.items():
            weight = self.criteria_weights.get(criterion, 1.0)
            prompt += f"- {criterion.capitalize()} (weight: {weight:.1f}): {description}\n"
        
        prompt += f"""
For each criterion, provide:
1. A score from 1 to {self.scale} where {self.scale} is the best
2. A detailed explanation for your score, including specific examples from the response
3. Suggestions for improvement if the score is below {self.scale}

Format your response as a valid JSON object with this structure:
{{
    "scores": {{
        "criterion1": score,
        "criterion2": score,
        ...
    }},
    "reasoning": {{
        "criterion1": "detailed explanation...",
        "criterion2": "detailed explanation...",
        ...
    }},
    "improvements": {{
        "criterion1": "suggestions for improvement...",
        "criterion2": "suggestions for improvement...",
        ...
    }}
}}
"""
        return prompt
    
    def evaluate(
        self, 
        query: str, 
        response: str, 
        reference: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> EvaluationResult:
        """
        Evaluate a response to a query.
        
        Args:
            query: The user query
            response: The AI response to evaluate
            reference: Optional reference answer for comparison
            metadata: Optional metadata to include
            
        Returns:
            An EvaluationResult object with scores and reasoning
        """
        if self.enable_logging:
            logger.info(f"Evaluating response for query: {query[:50]}...")
        
        prompt = self._build_prompt(query, response, reference)
        
        try:
            model_response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.temperature,
                response_format={"type": "json_object"},
            )
            
            content = model_response.choices[0].message.content
            evaluation = json.loads(content)
            
            return EvaluationResult(
                query=query,
                response=response,
                reference=reference,
                scores=evaluation.get("scores", {}),
                reasoning=evaluation.get("reasoning", {}),
                metadata={
                    **(metadata or {}),
                    "criteria_weights": self.criteria_weights,
                    "improvements": evaluation.get("improvements", {})
                }
            )
            
            if self.enable_logging:
                logger.info(f"Evaluation completed. Overall score: {result.overall_score():.2f}")
            
            return result
            
        except Exception as e:
            error_msg = f"Evaluation failed: {str(e)}"
            if self.enable_logging:
                logger.error(error_msg)
            raise RuntimeError(error_msg)
    
    def evaluate_batch(self, examples: List[Dict[str, str]]) -> List[EvaluationResult]:
        """
        Evaluate multiple examples.
        
        Args:
            examples: List of dictionaries with 'query', 'response', and optional 'reference' keys
            
        Returns:
            List of EvaluationResult objects
        """
        results = []
        for example in examples:
            result = self.evaluate(
                query=example["query"],
                response=example["response"],
                reference=example.get("reference"),
                metadata=example.get("metadata", {})
            )
            results.append(result)
        return results
    
    def calculate_scores(self, evaluations: List[EvaluationResult]) -> Dict[str, Any]:
        """
        Calculate aggregate scores from evaluations.
        
        Args:
            evaluations: List of EvaluationResult objects
            
        Returns:
            Dictionary with score statistics
        """
        if not evaluations:
            return {}
        
        # Extract all criteria
        all_criteria = set()
        for eval_result in evaluations:
            all_criteria.update(eval_result.scores.keys())
        
        # Aggregate scores
        results = {
            "count": len(evaluations),
            "overall": {
                "mean": np.mean([e.overall_score() for e in evaluations]),
                "median": np.median([e.overall_score() for e in evaluations]),
                "std": np.std([e.overall_score() for e in evaluations]),
                "min": min([e.overall_score() for e in evaluations]),
                "max": max([e.overall_score() for e in evaluations]),
            },
            "criteria": {}
        }
        
        # Calculate metrics for each criterion
        for criterion in all_criteria:
            scores = [e.scores.get(criterion, np.nan) for e in evaluations]
            scores = [s for s in scores if not np.isnan(s)]
            
            if not scores:
                continue
                
            results["criteria"][criterion] = {
                "mean": np.mean(scores),
                "median": np.median(scores),
                "std": np.std(scores),
                "min": min(scores),
                "max": max(scores),
            }
        
        return results
    
    def to_dataframe(self, evaluations: List[EvaluationResult]) -> pd.DataFrame:
        """
        Convert evaluation results to a DataFrame.
        
        Args:
            evaluations: List of EvaluationResult objects
            
        Returns:
            Pandas DataFrame with evaluation results
        """
        data = []
        
        for eval_result in evaluations:
            row = {
                "query": eval_result.query,
                "response": eval_result.response,
                "reference": eval_result.reference,
                "overall_score": eval_result.overall_score(),
            }
            
            # Add individual criterion scores
            for criterion, score in eval_result.scores.items():
                row[f"score_{criterion}"] = score
            
            # Add reasoning
            for criterion, reason in eval_result.reasoning.items():
                row[f"reason_{criterion}"] = reason
                
            # Add metadata
            for key, value in eval_result.metadata.items():
                row[f"meta_{key}"] = value
                
            data.append(row)
        
        return pd.DataFrame(data)
    
    def plot_scores(self, evaluations: List[EvaluationResult], figsize: tuple = (10, 6)) -> plt.Figure:
        """
        Plot score distribution across criteria.
        
        Args:
            evaluations: List of EvaluationResult objects
            figsize: Figure size
            
        Returns:
            Matplotlib figure
        """
        if not evaluations:
            # Create an empty plot with a message if no evaluations
            fig, ax = plt.subplots(figsize=figsize)
            ax.text(0.5, 0.5, "No evaluation data available", 
                   horizontalalignment='center', verticalalignment='center',
                   transform=ax.transAxes)
            ax.set_axis_off()
            return fig
            
        df = self.to_dataframe(evaluations)
        
        # Get score columns
        score_cols = [col for col in df.columns if col.startswith('score_')]
        
        if not score_cols:
            score_cols = ['overall_score']
            
        # Check if we have any valid scores
        if df[score_cols].isnull().all().all():
            fig, ax = plt.subplots(figsize=figsize)
            ax.text(0.5, 0.5, "No score data available", 
                   horizontalalignment='center', verticalalignment='center',
                   transform=ax.transAxes)
            ax.set_axis_off()
            return fig
        
        fig, ax = plt.subplots(figsize=figsize)
        
        # Rename columns for display
        df_plot = df[score_cols].copy()
        df_plot.columns = [col.replace('score_', '') for col in score_cols]
        
        # Create box plot (dropna=False to keep empty boxes for categories with no data)
        df_plot.boxplot(ax=ax, grid=False, return_type='dict')
        ax.set_title('Distribution of Scores by Criterion')
        ax.set_ylabel('Score')
        
        # Set y-axis limits to a sensible range based on the scale
        ax.set_ylim(0, self.scale + 0.5)
        
        plt.tight_layout()
        return fig 