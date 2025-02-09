import random
from typing import List

import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile

from src.chatbot import Chatbot, ChunkEvent, Message, Role, SourceEvent, create_history
from src.file_loader import load_uploaded_file


LOADING_MESSAGES = [
    "Adjusting Bell Curves",
    "Aligning Covariance Matrices",
    "Applying Feng Shui Shaders",
    "Bureacritizing Bureaucracies",
    "Calculating Inverse Probability Matrices",
    "Calculating Llama Expectoration Trajectory",
    "Calibrating Blue Skies",
    "Charging Ozone Layer",
    "Coalescing Cloud Formations",
    "Compounding Inert Tessellations",
    "Compressing Grammar Files",
    "Deciding What Message to Display Next",
    "Decomposing Singular Values"
    "Fixing Election Outcome Matrix",
    "Gathering Particle Sources",
    "Hiding Willio Webnet Mask",
    "Implementing Impeachment Routine",
    "Lecturing Errant Subsystems",
    "Modeling Object Components",
    "Mopping Occupant Leaks",
    "Normalizing Power",
    "Obfuscating Quigley Matrix",
    "Perturbing Matrices"
    "Projecting Law Enforcement Pastry Intake",
    "Realigning Alternate Time Frames",
    "Reconfiguring User Mental Processes",
    "Resolving GUID Conflict",
    "Reticulating Splines",
    "Routing Neural Network Infanstructure",
    "Searching for Llamas",
    "Seeding Architecture Simulation Parameters",
    "Sequencing Particles",
    "Setting Inner Deity Indicators",
    "Setting Universal Physical Constants",
    "Speculating Stock Market Indices",
    "Synthesizing Gravity",
    "Time-Compressing Simulator Clock",
    "Weathering Buildings"
]

WELCOME_MESSAGE = Message(role=Role.ASSISTANT, content="Hello! How can I help you today?")

st.set_page_config(
    page_title="RAG", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.header("RAG")
st.subheader("Private intelligence for your thoughts and files")

@st.cache_resource(show_spinner=False)
def create_chatbot(files: List[UploadedFile]):
    files = [load_uploaded_file(file) for file in files]
    return Chatbot(files)


def show_uploaded_documents() -> List[UploadedFile]:
    holder = st.empty()
    with holder.container():
        uploaded_files = st.file_uploader(
            label="Upload pdf files", type=["pdf", "md", "txt"], accept_multiple_files=True
        )

    if not uploaded_files:
        st.warning("Please upload PDF documents to continue!")
        st.stop()

    with st.spinner("Analyzing your document(s)..."):
        holder.empty()
        return uploaded_files
    
uploaded_files = show_uploaded_documents()
chatbot = create_chatbot(uploaded_files)

if "messages" not in st.session_state:
    st.session_state.messages = create_history(WELCOME_MESSAGE)

with st.sidebar:
    st.title("Your Files")
    file_list_text = "\n".join([f"- {file.name}" for file in chatbot.files])
    st.markdown(file_list_text)

for message in st.session_state.messages:
    with st.chat_message(message.role.value):
        st.markdown(message.content)

if prompt := st.chat_input("Type your message ..."):
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        full_response = ""
        message_placeholder = st.empty()
        message_placeholder.status(random.choice(LOADING_MESSAGES), state="running")
        for event in chatbot.ask(prompt, st.session_state.messages):
            if isinstance(event, SourceEvent):
                for i, doc in enumerate(event.context):
                    with st.expander(f"Source #{i + 1}"):
                        st.markdown(doc.page_content)
            if isinstance(event, ChunkEvent):
                chunk = event.content
                full_response += chunk
                message_placeholder.markdown(full_response)
