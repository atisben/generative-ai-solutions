# Image and Video Processing and Analysis with Python

This repository contains a comprehensive Python-based solution for processing and analyzing image and video data. It focuses on extracting meaningful insights from visual content, particularly for advertising analysis, by leveraging a combination of image processing techniques, GenAI models, and cloud storage. 

## Overview

The primary goal of this project is to:

1.  **Extract and Deduplicate Image and Video Data:** Fetch image and video URLs from a data source, process them, and deduplicate them using perceptual hashing for images.
2.  **Analyze Visual Content:** Use GenAI models to extract features and metadata from images and videos, gaining a deeper understanding of their content (product, style, text, etc).
3.  **Store and Manage Data:** Utilize Google Cloud Storage for image and video storage and BigQuery for data storage and manipulation.
4.  **Automate workflows** Make use of the Octocloud script to automate the different data manipulation.

## Key Features

*   **Image Processing:** 
    *   Image fetching from URLs and cloud storage.
    *   Perceptual hashing (dHash) for near-duplicate detection.
    *   Calculation of image aspect ratios.
*   **Video Processing:**
    *   Video metadata extraction (size, aspect ratio).
*   **Feature Extraction with GenAI:**
    *   Integration with Google's Gemini 2.0 Flash Experimental model.
    *   Extraction of structured information from images and videos such as product type, presence of text, brand logos, promotions, call to action, car brand, style, and more.
    *   Data models defined using Pydantic for type-safe data handling.
*   **Cloud Integration:**
    *   Google Cloud Storage for fetching image and video data.
    *   Google BigQuery for storing intermediate and final processed data.
*   **Cost Estimation:**
    *   Token usage tracking and cost estimation for GenAI model usage.
*   **Data Pipeline:**
    *   Automated end-to-end data pipeline from raw data import to final feature-enriched tables.
    *   Creation of intermediate tables to ensure the smooth running of the data flow.
*   **Libraries and Tools:**
    *   **Python Libraries**: `requests`, `base64`, `pandas`, `PIL`, `hashlib`, `tqdm`, `dotenv`, `google.cloud.bigquery`, `google.cloud.storage`, `cv2`.
    *   **LangChain**: `AzureChatOpenAI`, `BaseModel`, `Field`, `HumanMessage`, `chain`, `JsonOutputParser`.
    *   **GenAI**: Google GenAI.

## Workflow

The notebook follows these main steps:

1.  **Setup and Initialization:** Import required libraries, load environment variables using `dotenv`, configure pandas display.
2.  **Data Import:** Retrieve image and video URLs from Google BigQuery.
3.  **Image Processing:**
    *   Deduplicate images using perceptual hashing.
    *   Calculate aspect ratios.
    *   Store intermediate results in BigQuery.
    *   Extract features from deduplicated images using a GenAI model.
    *   Clean and transform extracted features.
    *   Store processed image features in a final BigQuery table.
4.  **Video Processing:**
    *   Extract video metadata such as size and aspect ratio.
    *   Store intermediate results in BigQuery.
    *   Extract features from videos using a GenAI model.
    *    Clean and transform extracted features.
    *    Store processed video features in a final BigQuery table.
5.  **Data Reconstitution** Reconstitute the final table to link all the features to the raw ads table

## Getting Started

To use this repository:

1.  **Clone the repository.**
2.  **Set up a Python virtual environment** and install all dependencies by running `pip install -r requirements.txt`
3.  **Set up the `.env` file** with your project-specific configurations (Google Cloud Project ID, API Keys, etc.) following the `.env.sample` example.
4.  **Execute the main notebook** to run the image and video processing workflow.

## Contributing

Contributions to this project are welcome. Feel free to submit pull requests.

## License

[Insert your License]