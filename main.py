import pandas as pd
from dotenv import load_dotenv
from StudyLabelGenerator import StudyLabelGenerator

# Load environment variables from the .env file
load_dotenv()

# Example usage:
if __name__ == "__main__":
    # Initialize the class (API key will be automatically loaded from .env if not provided)
    generator = StudyLabelGenerator()
    
    # Read the CSV file
    df = pd.read_csv('first30.csv')
    df = df[2:4]
    print(f'Usando solo {len(df)} filas.')
    # Preallocate lists to store results
    study_on = []
    study_types = []
    inclusion_criteria_list = []
    exclusion_criteria_list = []

    # Iterate through the DataFrame and generate labels for each study
    for index, row in df.iterrows():
        title = row['Title']
        abstract = row['Abstract']
        keywords = row['Keywords']

        # Call the generate_labels function which returns a list [Str, Str, Bool, Bool]
        labels = generator.generate_labels(title, abstract, keywords)

        # Append results to respective lists
        study_on.append(labels["study_on"])
        study_types.append(labels["study_type"])
        inclusion_criteria_list.append(labels["inclusion_criteria"])
        exclusion_criteria_list.append(labels["exclusion_criteria"])

    # Add the lists to the DataFrame as new columns
    df['Study_On'] = study_on
    df['Study_Type'] = study_types
    df['Inclusion_Criteria'] = inclusion_criteria_list
    df['Exclusion_Criteria'] = exclusion_criteria_list

    # Generate the labels
    print(df)
