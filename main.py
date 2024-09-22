import openai
import os
import json
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Set the API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load the JSON file with labels prompts
with open('labels_definition.json') as f:
    labels_definition = json.load(f)

# Define a function to generate labels
def generate_labels(title, abstract, keywords):
    # Extract different parts from the JSON
    study_on = labels_definition['study_on']
    study_type = labels_definition['study_type']
    inclusion_criteria = "\n".join(labels_definition['inclusion_criteria'])
    exclusion_criteria = "\n".join(labels_definition['exclusion_criteria'])
    
    # Construct the messages for the chat-based model
    messages = [
        {"role": "system", "content": "You are an expert in classifying scientific studies."},
        {"role": "user", "content": (f'Given the following scientific paper with the title: "{title}", '
                                     f'abstract: "{abstract}", and keywords: "{keywords}", '
                                     f'provide a list of labels separated by commas. The labels should be: '
                                     f'\n - In which system was the study done, choose one of {study_on}'
                                     f'\n - What type of study is it, choose one of {study_type}.'
                                     f'\n - Does it meet the inclusion criteria (True or False): {inclusion_criteria}'
                                     f'\n - Does it meet the exclusion criteria (True or False): {exclusion_criteria}'
                                     f'\n\n Example output: "humans, clinical trial, True, False"')
        }
    ]
    
    # Call the OpenAI API using the chat completions endpoint
    response = openai.chat.completions.create(
        model="gpt-4",  # Or "gpt-3.5-turbo"
        messages=messages,
        max_tokens=10,  # Short response expected
        temperature=0  # Set temperature for consistent output
    )
    
    # Extract and clean the response
    label = response.choices[0].message.content.strip().lower()
    
    return label

# Example usage
title = "Effects of a new drug on humans"
abstract = "The effectiveness of a new drug was evaluated in 100 human patients..."
keywords = "effectiveness, new drug, humans, patients"

label = generate_labels(title, abstract, keywords)
print(f"The study was conducted on: {label}")
