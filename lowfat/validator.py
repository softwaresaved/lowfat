"""
Validator functions
"""
from urllib import request

from django.core.exceptions import ValidationError

import PyPDF2

def online_document(url):
    """Check if online document is available."""
    online_resource = request.urlopen(url)

    # Need to test if website didn't redirect the request to another resource.
    if url != online_resource.geturl() or online_resource.getcode() != 200:
        raise ValidationError("Can't access online document.")

def pdf(value):
    """Check if filename looks like a PDF file."""

    filename = value.name.lower()

    if not filename.endswith(".pdf"):
        raise ValidationError("File name doesn't look to be a PDF file.")

    try:
        pdf_file = PyPDF2.PdfFileReader(value.file)  # pylint: disable=unused-variable
    except:
        raise ValidationError("File doesn't look to be a PDF file.")
