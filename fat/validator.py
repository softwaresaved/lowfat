"""o
Validator functions
"""
from django.core.exceptions import ValidationError
import PyPDF2

def pdf(value):
    """Check if filename looks like a PDF file."""

    filename = value.name.lower()
    
    if not filename.endswith(".pdf"):
        raise ValidationError("File name doesn't look to be a PDF file.")
    
    try:
        pdf = PyPDF2.PdfFileReader(value.file)
    except:
        raise ValidationError("File doesn't look to be a PDF file.")
