```markdown
# Introduction to Image Processing and Analysis with Python

## Description
This notebook provides a comprehensive guide to processing and analyzing images using Python. It leverages various libraries and tools to fetch, manipulate, and analyze images, particularly focusing on extracting and deduplicating image data, as well as integrating with cloud services for data storage and processing. The notebook also includes video analysis.

## Installation
To run this notebook, you will need to have the following libraries installed:

```bash
pip install requests
pip install pandas
pip install Pillow
pip install hashlib
pip install tqdm
pip install python-dotenv
pip install google-cloud-bigquery
pip install google-cloud-storage
pip install langchain-openai
pip install langchain
pip install google-generativeai
pip install pydantic
pip install typing-extensions
pip install ipython
```
You will also need to set up a `.env` file with the following variables:
```
PROJECT_ID="your_gcp_project_id"
```
## Usage
1.  **Set up the environment:**
    *   Install the required libraries using the `pip install` command above.
    *   Create a `.env` file in the same directory as the notebook and add your Google Cloud Project ID.
2.  **Run the notebook:**
    *   Open the Jupyter notebook.
    *   Execute each cell sequentially.

## Contents
1.  **Setup and Initialization:**
    *   Imports necessary libraries.
    *   Loads environment variables from the `.env` file.
    *   Configures pandas display options.
2.  **Data Import:**
    *   Retrieves image and video data from Google BigQuery using SQL queries.
    *   Filters data based on payer and media type (image or video).
    *   Loads data into pandas DataFrames.
3.  **Data Cleaning: Image Deduplication and Perceptual Hashing:**
    *   Defines a function `dhash` to generate perceptual hashes for images.
    *   Defines functions to load images from Google Cloud Storage (`image_to_bytes`, `image_to_pillow`).
    *   Calculates image aspect ratios.
    *   Applies the `dhash` function to each image in the DataFrame and stores the hash, size and aspect ratio.
    *   Exports the intermediate table to BigQuery.
4.  **Feature Extraction from images:**
    *   Groups images by their hash to identify duplicates.
    *   Uses Google Gemini to analyze the content of the images and extract features.
    *   Defines a Pydantic model `ImageInformation` to structure the extracted features.
    *   Prints the extracted features in JSON format.
    *   Estimates the cost of the image analysis.
5.  **Feature Extraction from videos:**
    *   Defines a Pydantic model `VideoInformation` to structure the extracted features.
    *   Uses Google Gemini to analyze the content of the videos and extract features.
    *   Prints the extracted features in JSON format.
    *   Estimates the cost of the image analysis.

## Examples
*   **Image Dataframe:**
    The notebook loads image data from BigQuery into a pandas DataFrame. The first few rows of the DataFrame are displayed.
    ```
    ad_creation_time ad_delivery_stop_time ad_delivery_start_time ad_active_status client_id
    0	2024-09-02	2024-10-01	2024-09-02	INACTIVE	Rei
    1	2024-09-02	2024-10-01	2024-09-02	INACTIVE	Rei
    2	2024-09-02	2024-10-01	2024-09-02	INACTIVE	Rei
    3	2024-09-02	2024-09-30	2024-09-02	INACTIVE	Rei
    4	2024-09-02	2024-09-30	2024-09-02	INACTIVE	Rei
    ```
*   **Image Analysis Output:**
    The notebook uses Google Gemini to analyze the content of the images and extract features. The output is a JSON object containing the extracted features.
    ```json
    {
        "actions": [],
        "actions_presence": false,
        "black_bars": false,
        "brand_logo": true,
        "call_to_action": false,
        "color_palette": ["gray", "red", "black"],
        "contrast_presence": true,
        "electric_vehicle": false,
        "environment": "outdoor",
        "human_presence": false,
        "image_description": "A gray Mini Countryman with a red roof is shown from the rear, parked on a red surface with a selection of color and wheel options displayed below.",
        "imagery_type": "3D rendering",
        "main_objects": ["car"],
        "new_old_vehicle": "new",
        "price": false,
        "product_elements": ["car", "color options", "wheel options"],
        "product_percent": 80,
        "product_presence": true,
        "product_type": "car",
        "product_usage": false,
        "promotion": false,
        "promotion_deadline": false,
        "promotion_display": false,
        "style": ["modern", "clean"],
        "text": true,
        "time_of_day": "daytime",
        "ad_purpose": "None",
        "background_main_color": "white",
        "call_to_action_size": 0,
        "call_to_action_verb": "None",
        "car_brand": "Mini",
        "car_model": "Countryman",
        "goal_awareness_or_consideration_or_conversion": "consideration",
        "human_age": "adult",
        "human_elements": [],
        "human_genders": [],
        "human_number": 0,
        "human_shot_size": [],
        "price_size": 0,
        "promotion_theme": "None",
        "promotion_tone": "None",
        "promotion_wording_type": "None",
        "text_extraction": "MINI COUNTRYMAN",
        "text_length": 1,
        "text_location": "center",
        "weather": "sunny"
    }
    ```
*   **Video Analysis Output:**
    The notebook uses Google Gemini to analyze the content of the videos and extract features. The output is a JSON object containing the extracted features.
    ```json
    {
        "actions": ["talking"],
        "actions_presence": true,
        "black_bars": false,
        "brand_logo": true,
        "call_to_action": false,
        "color_palette": ["yellow", "blue", "white"],
        "contrast_presence": true,
        "electric_vehicle": true,
        "environment": "indoor",
        "human_presence": true,
        "image_description": "A woman in a blue suit is talking to the camera.",
        "imagery_type": "photographs",
        "main_objects": ["woman", "sofa"],
        "new_old_vehicle": "new",
        "price": false,
        "product_elements": ["car"],
        "product_percent": 10,
        "product_presence": true,
        "product_type": "car",
        "product_usage": false,
        "promotion": false,
        "promotion_deadline": false,
        "promotion_display": false,
        "style": ["modern"],
        "text": true,
        "time_of_day": "daytime",
        "ad_purpose": "inform",
        "background_main_color": "yellow",
        "call_to_action_size": 0,
        "call_to_action_verb": "None",
        "car_brand": "Renault",
        "car_model": "Renault 5 E-Tech electric",
        "goal_awareness_or_consideration_or_conversion": "awareness",
        "human_age": "adult",
        "human_elements": ["woman with long blonde hair"],
        "human_genders": ["female"],
        "human_number": 1,
        "human_shot_size": ["medium shot"],
        "price_size": 0,
        "promotion_theme": "None",
        "promotion_tone": "informative",
        "promotion_wording_type": "None",
        "text_extraction": "Oh. I received a message. Aur�lien planet Cl�a, it's your turn! Okay, right on the topic.",
        "text_location": "down",
        "weather": "None"
    }
    ```

## Contributing
If you would like to contribute to this notebook, please follow these guidelines:
*   Fork the repository.
*   Create a new branch for your changes.
*   Make your changes and commit them with clear messages.
*   Submit a pull request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```
