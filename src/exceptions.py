"""
A module to store a few custom exception objects used across the project
"""


class UserInputError(Exception):
    """
    Python exception raised when user input is incorrect
    """

    code = 400
    description = "Invalid form input"


class OutputFormatError(Exception):
    """
    Python exception raised output format is incorrect
    """

    code = 500
    description = "llm"


class DBError(Exception):
    """
    Python exception raised when there is a MongoDB related issue.
    """

    code = 500
    description = "Could not connect to database"
