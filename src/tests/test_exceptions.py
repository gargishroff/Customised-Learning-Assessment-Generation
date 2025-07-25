"""
pytest based unit testing for everything in exceptions.py
"""

import pytest

from exceptions import OutputFormatError, UserInputError, DBError


class TestUserInputError:
    """
    A group of tests that test UserInputError
    """

    def test_exception(self):
        """
        Test that UserInputError is an Exception type
        """
        assert issubclass(UserInputError, Exception)

    def test_attributes(self):
        """
        Test that UserInputError has expected attributes
        """
        exc = UserInputError("hello")
        assert exc.code == 400
        assert exc.args == ("hello",)


class TestOutputFormatError:
    """
    A group of tests that test OutputFormatError
    """

    def test_exception(self):
        """
        Test that OutputFormatError is an Exception type
        """
        assert issubclass(OutputFormatError, Exception)

    def test_attributes(self):
        """
        Test that OutputFormatError has expected attributes
        """
        exc = OutputFormatError("hello")
        assert exc.code == 500
        assert exc.description == "llm"
        assert exc.args == ("hello",)


class TestDBError:
    """
    A group of tests that test DBError
    """

    def test_exception(self):
        """
        Test that DBError is an Exception type
        """
        assert issubclass(DBError, Exception)

    def test_attributes(self):
        """
        Test that DBError has expected attributes
        """
        exc = DBError("hello")
        assert exc.code == 500
        assert exc.args == ("hello",)


if __name__ == "__main__":
    pytest.main()
