from dotenv import load_dotenv
from StudyLabelGenerator import StudyLabelGenerator

# Load environment variables from the .env file
load_dotenv()

# Example usage:
if __name__ == "__main__":
    # Initialize the class (API key will be automatically loaded from .env if not provided)
    generator = StudyLabelGenerator()

    # Define the study details
    title = "Effects of a new drug on humans"
    abstract = "The effectiveness of a new drug was evaluated in 100 human patients..."
    keywords = "effectiveness, new drug, humans, patients"

    # Generate the labels
    labels = generator.generate_labels(title, abstract, keywords)
    print(labels)
