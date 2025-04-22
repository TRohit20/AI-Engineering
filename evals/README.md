# 🧠 Evals - LLM as a Judge

> Leverage LLMs to evaluate and improve LLM outputs with advanced consistency, objective metrics and weighted scoring

Evals is a simple, yet effective evaluation framework that uses state-of-the-art language models to assess and improve the quality of AI-generated content. It goes beyond simple scoring to provide detailed analysis, improvement suggestions, and visualizations of LLM outputs.

## ✨ Key Features

- **Customizable Criteria** - Define exactly what aspects of responses you want to evaluate
- **Consistent Scoring** - Get reliable 1-5 scale ratings across multiple dimensions
- **Detailed Reasoning** - Understand exactly why each score was assigned
- **Batch Processing** - Evaluate hundreds of examples efficiently
- **Rich Analytics** - Generate statistical summaries and visualizations
- **Simple Integration** - Just a few lines of code to get started

## 🚀 Quick Setup

```bash
# 1. Clone the repository
git clone https://github.com/TRohit20/AI-Engineering.git
cd evals

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up your OpenAI API key in a .env file
echo "OPENAI_API_KEY=your_api_key_here" > .env

# 5. Run the demonstration
python demo.py
```

> 💡 Make sure to replace `your_api_key_here` with your actual OpenAI API key. You can get one from [OpenAI's platform](https://platform.openai.com/api-keys).

## 📊 Usage Examples

### Basic Evaluation

```python
from evals import Evals

# Create evaluator with custom criteria
evaluator = Evals(
    model="gpt-4o",
    criteria={
        "accuracy": "Is the information accurate and factual?",
        "completeness": "Does the response address all aspects?",
        "clarity": "Is the response clear and well-structured?",
        "depth": "Does the response provide sufficient detail?",
        "originality": "Does the response show unique insights?"
    },
    criteria_weights={
        "accuracy": 1.5,
        "completeness": 1.2,
        "clarity": 1.0,
        "depth": 1.0,
        "originality": 0.8
    }
)

# Evaluate a single response
result = evaluator.evaluate(
    query="What is machine learning?",
    response="Machine learning is a type of AI that learns from data.",
    reference="Machine learning is a field of AI where systems learn from data to make decisions without explicit programming."
)

# View detailed results
print(f"Overall score: {result.overall_score():.2f}")
for criterion, score in result.scores.items():
    print(f"\n{criterion.capitalize()} (score: {score}/5):")
    print(f"Reasoning: {result.reasoning.get(criterion)}")
    print(f"Suggestions: {result.metadata['improvements'].get(criterion)}")
```

### Process Multiple Examples & Create Visualizations

```python
# Batch evaluate multiple examples
evaluations = evaluator.evaluate_batch([
    {
        "query": "What's the capital of France?",
        "response": "Paris is the capital of France.",
        "reference": "Paris is the capital and most populous city of France."
    },
    # Add more examples...
])

# Generate comprehensive statistics
scores = evaluator.calculate_scores(evaluations)
print(f"Overall mean score: {scores['overall']['mean']:.2f}")
print(f"Score range: {scores['overall']['min']:.2f} - {scores['overall']['max']:.2f}")

# Export to CSV for further analysis
df = evaluator.to_dataframe(evaluations)
df.to_csv('evaluation_results.csv', index=False)

# Create visualization
fig = evaluator.plot_scores(evaluations)
fig.savefig('score_distribution.png', dpi=300)
```

## 💡 Use Cases

- **Model Development** - Compare different models or versions
- **Prompt Engineering** - Test and optimize prompts
- **Quality Assurance** - Ensure AI outputs meet standards
- **Content Analysis** - Evaluate factuality and quality
- **Educational Assessment** - Grade and provide feedback on student work
- **Research Analysis** - Evaluate research paper summaries
- **Technical Documentation** - Assess documentation quality

## 🛠️ Advanced Options

### Custom Criteria and Weights

```python
# Use a different model or custom criteria
evaluator = Evals(
    model="gpt-4-turbo",
    temperature=0.2,
    scale=10,  # Use a 10-point scale instead of default 5
    criteria={
        "technical_accuracy": "Is the technical content accurate?",
        "practical_applicability": "Can the information be applied in practice?",
        "innovation": "Does it demonstrate innovative thinking?",
        "accessibility": "Is it understandable to the target audience?"
    },
    criteria_weights={
        "technical_accuracy": 2.0,
        "practical_applicability": 1.5,
        "innovation": 1.2,
        "accessibility": 1.0
    }
)
```

### Enhanced Logging

```python
assessor = LLMQualityAssessor(
    enable_logging=True,
    log_level="DEBUG"  # Options: DEBUG, INFO, WARNING, ERROR
)
```

### Custom Visualization

```python
# Create custom visualizations
fig = assessor.plot_scores(
    evaluations,
    figsize=(14, 10),
    style="seaborn-darkgrid"
)
```

## 📈 Performance Considerations

- Uses efficient batch processing for multiple evaluations
- Implements caching for repeated evaluations
- Provides progress tracking for long-running assessments
- Supports parallel processing for large datasets

## 🔍 Example

Run the included demonstration:

```bash
python demo.py
```

## Contributing
Contributions are welcome! If you have suggestions for improvements or new features, please fork the repository and submit a pull request.