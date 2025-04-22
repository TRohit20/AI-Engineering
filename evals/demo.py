#!/usr/bin/env python3
"""
Basic Demonstration of using the Evals class to evaluate LLM responses.
"""

import os
import json
from dotenv import load_dotenv
from evals import Evals

# Load environment variables (including API key)
load_dotenv()

# Example data
EXAMPLES = [
    {
        "query": "What are the benefits of regular exercise?",
        "response": "Regular exercise helps strengthen muscles and improve cardiovascular health. It also boosts mood and energy levels.",
        "reference": "Regular exercise offers numerous benefits including improved cardiovascular health, increased strength, better mood, weight management, and reduced risk of chronic diseases. It also enhances sleep quality and cognitive function."
    },
    {
        "query": "Explain how photosynthesis works.",
        "response": "Photosynthesis is the process where plants use sunlight to convert carbon dioxide and water into glucose and oxygen. This process occurs in the chloroplasts of plant cells.",
        "reference": "Photosynthesis is the process by which green plants, algae, and some bacteria convert light energy, usually from the sun, into chemical energy stored in glucose and other organic compounds. During this process, carbon dioxide and water are converted into glucose and oxygen is released as a byproduct. The process takes place in the chloroplasts of plant cells, specifically in the thylakoid membranes where the light-dependent reactions occur."
    },
    {
        "query": "What is the capital of France?",
        "response": "The capital of France is Paris, which is also its largest city.",
        "reference": "Paris is the capital and most populous city of France, with a population of over 2 million people within its city limits."
    },
    {
        "query": "How does quantum computing differ from classical computing?",
        "response": "Quantum computing uses quantum bits (qubits) that can exist in multiple states simultaneously, unlike classical bits which are either 0 or 1.",
        "reference": "Quantum computing fundamentally differs from classical computing in several ways. While classical computers use bits that can be either 0 or 1, quantum computers use quantum bits (qubits) that can exist in a superposition of states. This allows quantum computers to perform certain calculations exponentially faster than classical computers. Additionally, quantum computers leverage quantum phenomena like entanglement and interference to process information in ways that classical computers cannot."
    }
]

def main():
    """Run a basic evaluation example."""
    
    # Check for OpenAI API key
    if not os.environ.get("OPENAI_API_KEY"):
        print("Error: OpenAI API key not found!")
        print("Please set your OPENAI_API_KEY environment variable")
        return
    
    # Create evaluator with custom criteria
    evaluator = Evals(
        model="gpt-4o",
        criteria={
            "accuracy": "Is the information provided in the response accurate and factual?",
            "completeness": "Does the response address all aspects of the query comprehensively?",
            "clarity": "Is the response clear, coherent, and well-structured?",
            "depth": "Does the response provide sufficient depth and detail?",
            "originality": "Does the response demonstrate original thinking and unique insights?"
        },
        criteria_weights={
            "accuracy": 1.5,  # Weight accuracy more heavily
            "completeness": 1.2,
            "clarity": 1.0,
            "depth": 1.0,
            "originality": 0.8
        },
        enable_logging=True
    )
    
    print(f"Evaluating {len(EXAMPLES)} examples...")
    
    # Evaluate all examples
    evaluations = evaluator.evaluate_batch(EXAMPLES)
    
    # Print results for each evaluation
    for i, result in enumerate(evaluations):
        print(f"\nExample {i+1}:")
        print(f"Query: {result.query}")
        print(f"Response: {result.response}")
        print(f"Overall score: {result.overall_score():.2f}")
        
        for criterion, score in result.scores.items():
            print(f"\n  {criterion.capitalize()} (score: {score}/{evaluator.scale}):")
            print(f"    Reasoning: {result.reasoning.get(criterion, 'No reasoning provided')}")
            if criterion in result.metadata.get('improvements', {}):
                print(f"    Suggestions: {result.metadata['improvements'][criterion]}")
    
    # Calculate aggregate scores
    scores = evaluator.calculate_scores(evaluations)
    
    print("\n=== Overall Evaluation Results ===")
    print(f"Number of examples: {scores['count']}")
    print(f"Overall mean score: {scores['overall']['mean']:.2f}")
    print(f"Score range: {scores['overall']['min']:.2f} - {scores['overall']['max']:.2f}")
    
    print("\n=== Scores By Criterion ===")
    for criterion, metrics in scores.get('criteria', {}).items():
        print(f"{criterion.capitalize()}:")
        print(f"  Mean: {metrics['mean']:.2f}")
        print(f"  Median: {metrics['median']:.2f}")
        print(f"  Std Dev: {metrics['std']:.2f}")
        print(f"  Range: {metrics['min']:.2f} - {metrics['max']:.2f}")
    
    # Create results directory if it doesn't exist
    os.makedirs('results', exist_ok=True)
    
    # Save results to CSV
    df = evaluator.to_dataframe(evaluations)
    df.to_csv('results/evaluation_results.csv', index=False)
    print("\nResults saved to results/evaluation_results.csv")
    
    # Create score distribution plot
    fig = evaluator.plot_scores(evaluations)
    fig.savefig('results/score_distribution.png', dpi=300, bbox_inches='tight')
    print("Score distribution plots saved to results/score_distribution.png")
    
    # Save raw evaluation results as JSON
    with open('results/evaluations.json', 'w') as f:
        json.dump([eval.model_dump() for eval in evaluations], f, indent=2)
    print("Raw evaluation data saved to results/evaluations.json")

if __name__ == "__main__":
    main() 