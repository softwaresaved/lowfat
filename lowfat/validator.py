"""Validator functions."""
import logging
import pathlib
import sys
from urllib import request
from urllib.error import HTTPError

from django.core.exceptions import ValidationError

import magic
import PyPDF2

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


def online_document(url):
    """Check if online document is available."""
    try:
        online_resource = request.urlopen(url)

    except HTTPError as exc:
        if exc.code == 410:
            # This is the code returned by Google Drive
            raise ValidationError("Online document was removed.") from exc

        if exc.code == 403:
            req = request.Request(url, headers={'User-Agent': "lowFAT"})
            online_resource = request.urlopen(req)

        else:
            raise ValidationError(
                "Error! HTTP status code is {}.".format(exc.code)) from exc

    # Need to test if website didn't redirect the request to another resource.
    if url != online_resource.geturl() or online_resource.getcode() != 200:
        raise ValidationError("Can't access online document.")


def pdf(value):
    """Check if filename looks like a PDF file."""

    filename = value.name.lower()

    if not filename.endswith(".pdf"):
        raise ValidationError("File name doesn't look to be a PDF file.")

    try:
        _ = PyPDF2.PdfFileReader(value.file)

    except:
        logger.warning('Exception caught by bare except')
        logger.warning('%s %s', *(sys.exc_info()[0:2]))

        raise ValidationError("File doesn't look to be a PDF file.")  # pylint: disable=raise-missing-from


def validate_document(value) -> None:
    """Check if file is a document.

    e.g. Word document or OpenOffice / LibreOffice.
    """
    filepath = pathlib.Path(value.name)
    if filepath.suffix not in {
        ".doc",
        ".docx",
        ".odt"
    }:
        raise ValidationError("File name doesn't look like a document.")

    mimetype = magic.from_file(value.file)
    if mimetype not in {
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/vnd.oasis.opendocument.text"
    }:
        logger.warning("Invalid MIME type for document '%s'", value.name)
        raise ValidationError("Document does not appear to be of required type.")
