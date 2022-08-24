"""Validator functions."""
import logging
import pathlib
import typing
from urllib import request
from urllib.error import HTTPError

from django.core.exceptions import ValidationError

import magic

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


def make_mimetype_validator(expected_types: typing.Mapping[str, typing.Collection[str]]):
    """Make a validator for a Django `FileField` which validates file extension and MIME type.

    :param expected_types: Dictionary mapping file extension to list of permitted MIME types.
    """
    def validator(value) -> None:
        """Django field validator for file extension and MIME type.

        Raises `ValidationError` if field value is invalid.
        """
        filepath = pathlib.Path(value.name)

        try:
            expected = expected_types[filepath.suffix]
            if magic.from_buffer(value.file.open("rb").file.read(), mime=True) not in expected:
                raise ValidationError(
                    "Document does not appear to be of expected type.")

        except KeyError as exc:
            raise ValidationError("Document has unexpected extension.") from exc

    return validator


validate_pdf = make_mimetype_validator({
    ".pdf": ["application/pdf"],
})
pdf = validate_pdf  # Name used in old migrations - kept for compatibility


validate_document = make_mimetype_validator({
    ".doc": [
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ],
    ".docx": [
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ],
    ".odt": ["application/vnd.oasis.opendocument.text"],
    ".pdf": ["application/pdf"],
})
