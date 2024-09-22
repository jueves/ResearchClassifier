import openai
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Set the API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define a function to generate labels
def generate_labels(title, abstract, keywords):
    # Construct the messages for the chat-based model
    messages = [
        {"role": "system", "content": "You are an expert in classifying scientific studies."},
        {"role": "user", "content": f'Given the following scientific paper with the title: "{title}", abstract: "{abstract}", and keywords: "{keywords}", determine if the study was conducted on humans, animals, in-vitro, or in other systems. Only respond with one of the following labels: "humans", "animals", "in-vitro", "others".'}
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

