# README  
   
## Overview  
   
This Python notebook is designed to automate the process of generating customized cover letters for job applications, specifically for technical roles such as Data Scientist and Machine Learning Engineer. The notebook leverages various libraries and APIs to extract relevant information from a CV and a job description, and then uses an AI model to generate a tailored cover letter.  
   
## Prerequisites  
   
Before running the notebook, ensure you have the following installed:  
   
- Python 3.12.7  
- Required Python libraries: `dotenv`, `langchain_core`, `langchain_openai`, `fitz` (PyMuPDF), `PIL` (Pillow), `markdown2`, `pdfkit`, `re`  
- Azure OpenAI account and API keys  
   
## Setup  
   
1. Clone the repository and navigate to the directory containing the notebook.  
2. Create a `.env` file and add your Azure OpenAI deployment name and API version:  
   ```plaintext  
   DEPLOYMENT_NAME=your_deployment_name  
   OPENAI_API_VERSION=your_api_version  
   ```  
   
3. Ensure you have your CV and job description files in the `data` directory:  
   - `cv.pdf`: Your CV in PDF format.  
   - `cl_template.txt`: Template for the cover letter.  
   - `job_description.txt`: Job description text file.  
   
## Notebook Structure  
   
The notebook is organized into the following sections:  
   
1. **Import Libraries and Load Environment Variables**:  
   - Import necessary libraries and load environment variables from the `.env` file.  
   - Enable autoreload to automatically reload imported modules before executing code.  
   
2. **Load Templates and Personal Information**:  
   - Read the cover letter template and job description from text files.  
   
3. **Extract Adapted Information from CV**:  
   - Convert a specific page of the CV PDF to a base64-encoded image for further processing.  
   
4. **Instantiate LLM Agent**:  
   - Create an instance of the Azure OpenAI model.  
   
5. **Information Extraction from CV**:  
   - Define a system message template and a human message template to instruct the AI model on how to extract relevant information from the CV based on the job description.  
   
6. **Generate Cover Letter**:  
   - Define a prompt template for the AI model to generate a cover letter using the extracted information and job description.  
   - Invoke the AI model to generate the cover letter.  
   
7. **Export PDF**:  
   - Convert the generated cover letter from Markdown to HTML and save it as a PDF.  
   
## Running the Notebook  
   
1. Ensure all prerequisites are met and the required files are in place.  
2. Open the notebook in Jupyter or any compatible environment.  
3. Execute the cells sequentially to process the information and generate the cover letter.  
4. The final cover letter will be saved as an HTML file in the `data` directory.  
   
## Output  
   
The notebook generates a customized cover letter tailored to the provided job description and CV. The final cover letter is saved in the `data` directory as `output.html`.  
   
## Conclusion  
   
This notebook provides an automated solution for generating professional cover letters tailored to specific job applications. By leveraging AI, it ensures that the cover letter highlights the most relevant skills and experiences, increasing the chances of securing an interview.