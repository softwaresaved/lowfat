"""
This module contains small utility classes and functions which do not clearly belong to one part of the project.
"""

import enum


class ChoicesEnum(enum.Enum):
    """
    Abstract Enum class to represent values in a Django CharField choices.
    """
    @classmethod
    def choices(cls):
        """
        Get the list of choices for this class.

        The name of the enum field is used as the human readable name.
        The value of the enum field is stored in the database.
        """
        return tuple((tag.value, tag.name) for tag in cls)
