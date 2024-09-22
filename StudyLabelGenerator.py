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

    def sanitize_openai_response(self, response):
        """
        Sanitize the response from openai.chat.completions.create().

        Args:
            response (str): The raw response from OpenAI API as a string.

        Returns:
            bool: True if the response is a valid dictionary and matches the structure, else False.
        """
        try:
            # Attempt to parse the response as a dictionary
            response_dict = json.loads(response)

            # Check if it has the correct structure
            expected_keys = {"study_on", "study_type", "inclusion_criteria", "exclusion_criteria"}

            # Verify that all required keys are present and their types are correct
            if (expected_keys.issubset(response_dict.keys()) and
                isinstance(response_dict["study_on"], str) and
                isinstance(response_dict["study_type"], str) and
                response_dict["inclusion_criteria"] in ["True", "False"] and
                response_dict["exclusion_criteria"] in ["True", "False"]):
                return True
            else:
                return False

        except json.JSONDecodeError:
            return False

    def get_openai_response(self, messages, temp=0):
        response = openai.chat.completions.create(
            model="gpt-4o-mini-2024-07-18",
            messages=messages,
            max_tokens=100,  # Short response expected
            temperature=temp  # Set temperature for consistent output
            )
        content = response.choices[0].message.content
        return(content)

    def get_valid_response(self, messages, max_tries=5, initial_temperature=0):
       """
       Try to get a valid response from OpenAI up to max_tries times,
       increasing the temperature after the first attempt.

       Args:
           messages (list): The chat messages to send to OpenAI API.
           max_tries (int): The maximum number of retry attempts.
           initial_temperature (float): The initial temperature for the first try.

       Returns:
           str: The valid response if found within the maximum attempts, else None.
       """
       temperature = initial_temperature

       for attempt in range(1, max_tries + 1):
           # Create the response with the current temperature
           response = self.get_openai_response(messages, temperature)

           if response and self.sanitize_openai_response(response):
            return response  # Return the valid response

           print("Response is invalid. Trying again...")

           # Increase the temperature for subsequent tries to introduce creativity
           temperature = min(temperature + 0.2, 1.0)  # Increase temperature, maxing out at 1.0

       print("Max attempts reached. No valid response found.")
       return None


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
                                         f'provide keys and values of a json file. The variables should be: '
                                         f'\n - In which system was the study done, choose one of {study_on}'
                                         f'\n - What type of study is it, choose one of {study_type}.'
                                         f'\n - Does it meet the inclusion criteria (True or False): {inclusion_criteria}'
                                         f'\n - Does it meet the exclusion criteria (True or False): {exclusion_criteria}'
                                         '\n\n Respond only with a json structure, no other comments or text.'
                                         '\nExample output: {"study_on": "humans","study_type": "observational study", "inclusion_criteria": "True", "exclusion_criteria": "False"}')
            }
        ]
        
        # Call the OpenAI API using the chat completions endpoint
        content = self.get_valid_response(messages)
        
        # Extract and clean the response
        labels = json.loads(content)
        boolean_keys = ['inclusion_criteria', 'exclusion_criteria']

        # Convert specific keys with boolean-like strings to actual booleans or set to None for invalid labels
        for key in boolean_keys:
            if key in labels:
                if labels[key].lower() == "true":
                    labels[key] = True
                elif labels[key].lower() == "false":
                    labels[key] = False
                else:
                    labels[key] = None                       
        return labels
