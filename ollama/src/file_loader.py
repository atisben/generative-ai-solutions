from dataclasses import dataclass
from pathlib import Path

from pypdfium2 import PdfDocument
from streamlit.runtime.uploaded_file_manager import UploadedFile

from src.config import Config

TEXT_FILE_EXTENSION = ".txt"
MD_FILE_EXTENSION = ".md"
PDF_FILE_EXTENSION = ".pdf"


# Usage of the File Dataclass:
 
# Simplicity in Declaration:
# The @dataclass decorator simplifies the creation of class instances by automatically generating the __init__ method. Without the decorator, you would have to manually define an initializer that sets the name and content attributes.
# Automatic __repr__ Method Generation:
# Dataclasses automatically generate a __repr__ method that is useful for debugging and logging purposes, as it provides a string representation of the dataclass instances which includes the values of its fields.
# Immutability Option:
# While not used in this snippet, dataclasses can easily be made immutable (read-only) by setting the frozen parameter to True, which can help prevent bugs in a larger system by making the instance's state unchangeable after initialization.
# Type Hints:
# Dataclasses support type hints, enhancing code readability and allowing for better static analysis and IDE support. In your example, name and content are explicitly marked as strings (str).
# Easy Comparison:
# Dataclasses also provide implementations for __eq__ (and optionally for ordering methods if order=True is set), which makes instances of the class easily comparable based on their fields.

@dataclass
class File:
    name: str
    content: str

def extract_pdf_content(data: bytes) -> str:
    pdf = PdfDocument(data)
    content = ""
    for page in pdf:
        text_page = page.get_textpage()
        content += f"{text_page.get_text_bounded()}\n"
    return content

def load_uploaded_file(uploaded_file: UploadedFile) -> File:
    file_extension = Path(uploaded_file.name).suffix
    if file_extension not in Config.ALLOWED_FILE_EXTENSIONS:
        raise ValueError(f"Invalid file extension: {file_extension} for file {uploaded_file.name}")
    if file_extension == PDF_FILE_EXTENSION:
        return File(name=uploaded_file.name, content=extract_pdf_content(uploaded_file.getvalue()))
    return File(name=uploaded_file.name, content=uploaded_file.getvalue().decode("utf-8"))