import openai
import os
import json

class StudyLabelGenerator:
    def __init__(self, api_key=None, json_file='labels_definition.json'):
        # Load environment variables if API key is not provided
        if api_key is None:
            self.api_key = os.getenv("OPENAI_API_KEY")
        else:
            self.api_key = api_key      
        openai.api_key = self.api_key

        # Load the JSON file with labels prompts
        with open(json_file) as f:
            self.labels_definition = json.load(f)

    def generate_labels(self, title, abstract, keywords):
        """ Generate labels for a scientific study based on the given inputs. """
        # Extract different parts from the JSON
        study_on = self.labels_definition['study_on']
        study_type = self.labels_definition['study_type']
        inclusion_criteria = "\n".join(self.labels_definition['inclusion_criteria'])
        exclusion_criteria = "\n".join(self.labels_definition['exclusion_criteria'])
        
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
                                         f'\n\n Example output: humans, clinical trial, True, False')
            }
        ]
        
        # Call the OpenAI API using the chat completions endpoint
        response = openai.chat.completions.create(
            model="gpt-4o-mini-2024-07-18",
            messages=messages,
            max_tokens=100,  # Short response expected
            temperature=0  # Set temperature for consistent output
        )
        
        # Extract and clean the response
        content = response.choices[0].message.content
        content_list = [item.strip() for item in content.split(',')]
        labels = [False if item.lower() == 'false' else True if item.lower() == 'true' else item for item in content_list]
                       
        return labels

