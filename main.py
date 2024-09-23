import textwrap
import pandas as pd
from dotenv import load_dotenv
from StudyLabelGenerator import StudyLabelGenerator


DATA_FILENAME="all_papers.csv"
METADATA_FILENAME="labels_definition.json"
SAMPLE=None
MIN_YEAR=2022
CREATE_LABELS=False

# Load environment variables from the .env file
load_dotenv()

def get_report(df, show_abstract=False, export=False):
    report = ""
    for index, row in df.iterrows():
        if show_abstract:
            title = "# " + row.Title
            abstract = "\n\n" + textwrap.fill(row.Abstract, width=60)
        else:
            title = f"**{row.Title}**"
            abstract = ""
        labels = (f"`Study on: {row.Study_On} | Study type: {row.Study_Type} |"
                  f"Inclusion_Criteria: {row.Inclusion_Criteria} | "
                  f"Exclusion_Criteria: {row.Exclusion_Criteria}`")
        
        report += f"{title}  \n{labels}{abstract}"
        report += "\n\n----------------------------\n\n"
    
    if export:
        file_name = "report.md"
        with open(file_name, "w") as file:
            file.write(report)
        print(f"Report written to {file_name}.")
    else:
        print(report)

def count_df(df):
    df = df[df.Year > 2010]
    print(f"After 2010: {len(df)}")

    df = df[df.Study_Type != "other"]
    print(f"With valid study type: {len(df)}")

    df = df[df.Study_On == "humans"]
    print(f"On humans: {len(df)}")

    # Exclude 'systematic review' and 'meta-analysis' with ~
    df = df[~df.Study_Type.isin(["systematic review", "meta-analysis"])]
    print(f'Without meta-analysis: {len(df)}')

    df = df[(df.Inclusion_Criteria == True) & (df.Exclusion_Criteria == False)]
    print(f"With valid inclusion and exclusion criteria: {len(df)}")

    #df = df[df.Year > MIN_YEAR]
    #print(f"After {MIN_YEAR}: {len(df)}")

    df = df[df["Publication Type"].isin(['Trial registry record', 'Journal article'])]
    print(f"Only Trial registry record and Journal article: {len(df)}")
    return df

if __name__ == "__main__" and CREATE_LABELS:
    # Initialize the class (API key will be automatically loaded from .env if not provided)
    generator = StudyLabelGenerator(json_file=METADATA_FILENAME)
    
    # Read the CSV file
    df = pd.read_csv(DATA_FILENAME)
    if SAMPLE:
        df = df.sample(SAMPLE)
    print(f'Iniciando el etiquetado de {len(df)} artículos...')
    
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
    df.to_csv("output.csv")

df = pd.read_csv("output.csv")
#get_report(df, show_abstract=False, export=True)


