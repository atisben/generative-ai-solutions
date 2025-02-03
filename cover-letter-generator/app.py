from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import os
import base64
import io
import fitz
from PIL import Image

load_dotenv()

import gradio as gr

# Open the template cover letter
with open('data/cl_template.txt', 'r') as file:  
    # Read the contents of the file  
    cl_template = file.read()  

# Open the CV
def pdf_page_to_base64(pdf_path: str, page_number: int):
    pdf_document = fitz.open(pdf_path)
    page = pdf_document.load_page(page_number - 1)  # input is one-indexed
    pix = page.get_pixmap()
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")

    return base64.b64encode(buffer.getvalue()).decode("utf-8")


base64_image = pdf_page_to_base64("data/cv.pdf", 0)

# Create an instance of Azure OpenAI
llm = AzureChatOpenAI(
    temperature=0,
    azure_deployment=os.getenv('DEPLOYEMENT_NAME'),
    openai_api_version=os.getenv('OPENAI_API_VERSION'),
    #rate_limiter=rate_limiter
    )

def generate_cl(company_name, job_description, language):

    # Step 1: extract information from the CV
    system_string = """
        You are an expert extracting information from CV for technical profiles, 
        specifically for roles such as Data Scientist and Machine Learning Engineer. 
        Extract relevant information from a CV that will help build a cover letter. 

        You are provided with a job description and a pdf file CV. Given the content of the job description, extract and summarize the most important information.
        """

    system_message = SystemMessage(
        content=[
            {"type": "text", "text": system_string},
        ]
    )

    human_message = HumanMessage(
        content=[
            {"type": "text", "text": """
                Content of the job desription:
                {job_description}
            
                Content of the CV:
            """},
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
            },
        ]

    )

    extraction_prompt = ChatPromptTemplate.from_messages([system_message, human_message])
    extraction_chain = extraction_prompt | llm 
    extracted_information = extraction_chain.invoke({"job_description": job_description})

    # Step 2: Craft the cover letter
    prompt = ChatPromptTemplate.from_messages([

        ("system", """You are an expert in crafting professional and compelling cover letters tailored for technical profiles, 
        specifically for roles such as Data Scientist and Machine Learning Engineer. 
        Your task is to create a cover letter that highlights the candidate's technical skills, 
        relevant experiences, and enthusiasm for the role they are applying for. 
        The cover letter should be concise, persuasive, and tailored to the specific job description provided.
        You are provided with a job description and a template cover letter that you can take into account to write an adapted cover letter:

        Here are the key elements to include:
        - Introduction:
        Briefly introduce the candidate and state the position they are applying for.
        Mention how they found the job posting and why they are excited about the opportunity.
        - Technical Skills and Experience:
        Highlight the candidate's relevant technical skills (e.g., programming languages, tools, frameworks).
        Describe their professional experience related to the role (e.g., past projects, research, employment history).
        Mention any notable achievements or contributions in their field.
        - Alignment with the Job Description:
        Tailor the cover letter to reflect how the candidate's skills and experiences align with the specific requirements of the job.
        Provide examples of how they have successfully applied their skills in past roles.
        - Passion and Fit:
        Convey the candidate's enthusiasm for the role and the company.
        Explain why they believe they are a great fit for the team and how they can contribute to the company’s success.
        - Conclusion:
        Summarize the key points and express eagerness to discuss the application further in an interview.
        Provide contact information and thank the reader for their time and consideration.
        
        Profile details:
        {profile_details}
         
        Profile details:
        {company_name}
        
        job description:
        {job_description}
        
        """
        )
    ])

    prompt_FR = ChatPromptTemplate.from_messages([

        ("system", """Vous êtes un expert dans la rédaction de lettres de motivation professionnelles et convaincantes, adaptées aux profils techniques, notamment pour des postes tels que Data Scientist et Machine Learning Engineer. Votre tâche consiste à créer une lettre de motivation qui met en avant les compétences techniques du candidat, ses expériences pertinentes et son enthousiasme pour le poste auquel il postule. La lettre de motivation doit être concise, persuasive et adaptée à la description de poste fournie. Vous disposez d'une description de poste et d'un modèle de lettre de motivation que vous pouvez prendre en compte pour rédiger une lettre de motivation adaptée :

    Voici les éléments clés à inclure :

    Introduction :
    Présentez brièvement le candidat et indiquez le poste auquel il postule. Mentionnez comment il a trouvé l'annonce et pourquoi il est enthousiaste à propos de cette opportunité.
    Compétences techniques et expérience :
    Mettez en avant les compétences techniques pertinentes du candidat (par exemple, langages de programmation, outils, frameworks). Décrivez son expérience professionnelle liée au poste (par exemple, projets passés, recherches, antécédents professionnels). Mentionnez les réalisations ou contributions notables dans son domaine.
    Alignement avec la description de poste :
    Adaptez la lettre de motivation pour refléter comment les compétences et expériences du candidat correspondent aux exigences spécifiques du poste. Fournissez des exemples de la manière dont il a appliqué avec succès ses compétences dans des rôles précédents.
    Passion et adéquation :
    Exprimez l'enthousiasme du candidat pour le poste et l'entreprise. Expliquez pourquoi il pense être un excellent candidat pour l'équipe et comment il peut contribuer au succès de l'entreprise.
    Conclusion :
    Résumez les points clés et exprimez votre impatience de discuter de la candidature plus en détail lors d'un entretien. Fournissez des informations de contact et remerciez le lecteur pour son temps et sa considération.
        
        Détails du profil:
        {profile_details}
         
        Nom de l'entreprise:
        {company_name}
        
        
        Description_du_poste
        {job_description}
        
        """
        )
    ])


    if language == "FR":
        cover_letter_chain = prompt_FR | llm 
    else:
        cover_letter_chain = prompt | llm 

    response = cover_letter_chain.invoke({
        "profile_details": extracted_information,
        "job_description": job_description,
        "company_name": company_name})
    return response.content

# UI

with gr.Blocks() as demo:
    company_name = gr.Textbox(label="Company Name")
    job_desc = gr.Textbox(label="Job Description")
    language = gr.Dropdown(["EN", "FR"], label="Language")
    output = gr.Markdown(label="Cover Letter")
    generate_button = gr.Button("Generate")
    generate_button.click(fn=generate_cl, inputs=[company_name, job_desc, language], outputs=output, api_name="generate_cover_letter")

if __name__ == "__main__":

    demo.launch()


