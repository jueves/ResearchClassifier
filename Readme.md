# ResearchClassifier

This project aims to assist in meta-analysis research by classifying a dataset of research papers. It uses the OpenAI Chat API to add tags for classification purposes.

### Dataset

The dataset primarily consists of search results from the [Cochrane Library](https://www.cochranelibrary.com/). However, it can be adapted to support search results from other research databases.

### Classification

The classification process is guided by specific criteria defined in a `labels_definition.json` file. The current criteria include:

- **`study_on`**: Identifies the study subject (animals, humans, in-vitro or other).
- **`study_type`**: Specifies the type of study (clinical trial, observational study, systematic review, meta-analysis or other).
- **`inclusion_criteria`**: Defines the conditions that an article must meet to be of interest. The article is considered relevant if it meets **all** specified criteria.
- **`exclusion_criteria`**: Outlines conditions that would make an article irrelevant. The article is excluded if it meets **any** of these criteria.

Classification is based on the tags, title, and abstract of each paper. One API call is made per article, with up to three additional attempts for correction if errors are detected.

### Current State

The current results do not meet the desired quality standards, rendering the project impractical for use in its current form, particularly with the GPT-4-o-mini model. The low performance may be due to the length and complexity of the abstracts, as well as the limitations of using only titles and tags for classification.

Given that the project is no longer required by the author, further development has been put on hold. However, future improvements could explore alternative models or different approaches to enhance classification accuracy.
