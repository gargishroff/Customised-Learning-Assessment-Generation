"""
pytest based unit testing for everything in userinput.py
"""

import pytest

from userinput import UserInputError, UserInput


class TestUserInput:
    """
    A group of tests that test UserInput
    """

    def test_constructor(self):
        """
        Test constructor method of UserInput
        """
        # First check all valid inputs
        topic = "Mathematics"
        question_type = "LA"
        num_questions = 10
        pdfs = ["math1.pdf", "math2.pdf"]
        context_keywords = "algebra, calculus"

        obj = UserInput(topic, question_type, num_questions, pdfs, context_keywords)

        # Check if attributes are set correctly
        assert obj.topic == topic
        assert obj.question_type == "Long Answer"
        assert obj.num_questions == num_questions
        assert obj.pdfs == pdfs
        assert obj.context_keywords == context_keywords.strip()

        # Invalid topic (not a string)
        with pytest.raises(UserInputError):
            UserInput(123, "SA", 5, ["example.pdf"])

        # Invalid question type (not a string)
        with pytest.raises(UserInputError):
            UserInput("Physics", 123, 5, ["example.pdf"])

        # Invalid num_questions (not an integer)
        with pytest.raises(UserInputError):
            UserInput("Chemistry", "LA", "five", ["example.pdf"])

        # Invalid pdfs (not a list)
        with pytest.raises(UserInputError):
            UserInput("Biology", "SA", 10, "example.pdf")

        # Invalid pdfs (not list of strings)
        with pytest.raises(UserInputError):
            UserInput("Biology", "SA", 10, [123, "example.pdf"])

        # Empty context_keywords
        obj = UserInput("History", "SA", 15, ["history.pdf"], "")
        assert obj.context_keywords == ""

        # Invalid context_keywords (not a string)
        with pytest.raises(UserInputError):
            obj = UserInput(
                "History", "SA", 15, ["history.pdf"], ["algebra", "calculus"]
            )

        # Check if leading/trailing whitespaces are stripped
        obj = UserInput("   Geography   ", "SA", 8, ["geo.pdf"], "  maps,  ")
        assert obj.topic == "Geography"
        assert obj.context_keywords == "maps,"

    def test_from_request_form(self):
        """
        Tests from_request_form method
        """
        # Valid request form dictionary, check attributes are correct
        request_form = {
            "topic": "Chemistry",
            "question_type": "SA",
            "num_questions": "10",
            "pdfs": '{"fileList":[{"name":"chemistry.pdf"},{"name":"organic.pdf"}]}',
            "context_keywords": "molecules, reactions",
        }

        obj = UserInput.from_request_form(request_form)

        assert obj.topic == "Chemistry"
        assert obj.question_type == "Short Answer"
        assert obj.num_questions == 10
        assert obj.pdfs == ["chemistry.pdf", "organic.pdf"]
        assert obj.context_keywords == "molecules, reactions"

        # Missing context_keywords in fields is allowed
        del request_form["context_keywords"]
        obj = UserInput.from_request_form(request_form)
        assert obj.context_keywords == ""

        # Missing pdfs in fields is also allowed
        del request_form["pdfs"]
        obj = UserInput.from_request_form(request_form)
        assert obj.pdfs == []

        # Missing topic field is not allowed
        del request_form["topic"]
        with pytest.raises(UserInputError):
            UserInput.from_request_form(request_form)

        # Incorrect field types in request form
        request_form = {
            "topic": "Physics",
            "question_type": "LA",
            "num_questions": "ten",  # Incorrect type
            "pdfs": '{"fileList":[{"name":"physics.pdf"}]}',
            "context_keywords": "laws, equations",
        }

        # Incorrect num_questions field type
        with pytest.raises(UserInputError):
            UserInput.from_request_form(request_form)

        # Incorrect pdfs field type
        request_form["num_questions"] = "5"  # Resetting to valid value
        request_form["pdfs"] = '{"fileList": "invalid"}'  # Incorrect type
        with pytest.raises(UserInputError):
            UserInput.from_request_form(request_form)

    def test_make_prompt(self):
        """
        Tests make_prompt method
        """

        obj = UserInput("Mathematics", "MCQ", 10, [], "algebra, calculus")
        prompt = obj.make_prompt()
        assert isinstance(prompt, str)

        # check all parameters are mentioned atleast once in prompt
        assert "Mathematics" in prompt
        assert "MCQ" in prompt
        assert "10" in prompt
        assert "algebra, calculus" in prompt


if __name__ == "__main__":
    pytest.main()
