import pandas as pd
from distlabel.llms import OllamaLLM
from distlabel.pipeline import Pipeline
from distilabel.steps import LoadDataFromhub
from distilabel.steps.tasks import TextGeneration, UltraFeedback
from distilabel.steps import GroupColumns

# Load two models of your choice 
model1 = OllamaLLM(model="llama3.1", timeout= 1000)
model2 = OllamaLLM(model="llama3.1:70b-instruct-q2_k", timeout= 1000)

with Pipeline(name="preference-datagen-llama3") as pipeline:
    
    # Load dataset with prompts
    load_dataset = LoadDataFromhub(
        name="laod_dataset",
        output_mappings={"prompt": "instruction"},
    )

    # Generate two responses
    generate = [
        TextGeneration(name="generate_response1", llm=model1),
        TextGeneration(name="generate_response2", llm=model2),
    ]

    # Combine the responses into one column
    combine = GroupColumns(
        columns=["generation", "model_name"],
        output_columns=["generations", "model_names"],
    )

    # Evaluate the responses with an LLM-as-a-judge 
    evaluate = UltraFeedback(
        aspect="overall-rating",
        llm=model2,
    )

    # Define and run the pipeline
    load_dataset >> generate >> combine >> evaluate
    
if __name__ == "__main__":
    distiset = pipeline.run(
        parameters={
            load_dataset.name: {
                "repo_id": "distilabel-internal-testing/instruction-dataset-mini",
                "split": "test",
            }
        },
    )
    