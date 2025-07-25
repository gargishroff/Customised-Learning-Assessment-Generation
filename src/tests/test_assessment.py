"""
pytest based unit testing for everything in assessment.py
"""

import string

import pytest

from assessment import (
    option_id_as_int,
    OutputFormatError,
    QuestionBase,
    QuestionLongAnswer,
    QuestionMCQ,
    QuestionSubjectiveAnswer,
    QuestionShortAnswer,
    Assessment,
)
from userinput import UserInput


class TestOptionIdAsInt:
    """
    A group of tests that test option_id_as_int
    """

    def test_int_inputs(self):
        """
        Test option_id_as_int handles an int by directly returning it
        """
        for i in range(4):
            assert option_id_as_int(i) == i

    def test_str_inputs(self):
        """
        Test option_id_as_int handles an str object correctly
        - must handle int-in-str
        - must handle alplabet-in-str
        - must handle any suffixes
        """
        for i in range(4):
            for suffix in ("", ".", ")"):
                assert option_id_as_int(f"{i}{suffix}") == i
                assert option_id_as_int(f"{string.ascii_lowercase[i]}{suffix}") == i
                assert option_id_as_int(f"{string.ascii_uppercase[i]}{suffix}") == i

    def test_invalid_inputs(self):
        """
        Any invalid input should error with OutputFormatError
        """
        for invalid_input in ("", "ab)", "testing", None, 2.3, [1], {3: "hello"}):
            with pytest.raises(OutputFormatError):
                option_id_as_int(invalid_input)


class TestQuestionBase:
    """
    A group of tests that test QuestionBase
    """

    def test_construction(self):
        """
        Test construction of QuestionBase
        """
        question = QuestionBase({"question": "What is your name?"})
        assert question.question == "What is your name?"
        assert question.question_type is None
        with pytest.raises(OutputFormatError):
            QuestionBase({})

    def test_update_question(self):
        """
        Test test_update_question method
        """
        question = QuestionBase({"question": "What is your name?"})
        question.update_question("How are you?")
        assert question.question == "How are you?"
        with pytest.raises(OutputFormatError):
            question.update_question(123)

    def test_to_dict(self):
        """
        Test to_dict method
        """
        question = QuestionBase({"question": "What is your name?"})
        with pytest.raises(RuntimeError):
            # abstract method, not implemented
            assert question.to_dict()


class TestQuestionSubjectiveAnswer:
    """
    A group of tests that test QuestionSubjectiveAnswer
    """

    def test_construction(self):
        """
        Test construction of QuestionSubjectiveAnswer
        """
        question = QuestionSubjectiveAnswer(
            {"question": "What is your name?", "sample_answer": "My name is John."}
        )
        assert question.question_type is None
        assert question.question == "What is your name?"
        assert question.sample_answer == "My name is John."
        with pytest.raises(OutputFormatError):
            QuestionSubjectiveAnswer({})

    def test_update_sample_answer(self):
        """
        Test update_sample_answer method
        """
        question = QuestionSubjectiveAnswer(
            {"question": "What is your name?", "sample_answer": "My name is John."}
        )
        question.update_sample_answer("My name is prakhar.")
        assert question.sample_answer == "My name is prakhar."
        with pytest.raises(OutputFormatError):
            question.update_sample_answer(123)

    def test_to_dict(self):
        """
        Test to_dict method
        """
        question = QuestionSubjectiveAnswer(
            {"question": "What is your name?", "sample_answer": "My name is John."}
        )
        with pytest.raises(RuntimeError):
            # abstract method, not implemented
            question.to_dict()


class TestQuestionMCQ:
    """
    A group of tests that test QuestionMCQ
    """

    def test_construction(self):
        """
        Test construction of QuestionMCQ
        """
        question = QuestionMCQ(
            {"question": "What is 1+1?", "options": ["1", "2"], "correct_answer": 1}
        )
        assert question.question_type == "MCQ"
        assert question.question == "What is 1+1?"
        assert question.options == ["1", "2"]
        assert question.correct_answer == 1
        with pytest.raises(OutputFormatError):
            QuestionMCQ({})

    def test_update_option(self):
        """
        Test update_option method
        """
        question = QuestionMCQ(
            {"question": "What is 1+1?", "options": ["1", "2"], "correct_answer": 1}
        )
        assert question.options == ["1", "2"]
        question.update_option("1", "3")
        assert question.options == ["1", "3"]
        question.update_option(0, "6")
        assert question.options == ["6", "3"]
        question.update_option("B.", "10")
        assert question.options == ["6", "10"]
        with pytest.raises(OutputFormatError):
            question.update_option("a", 3)

    def test_to_dict(self):
        """
        Test to_dict method
        """
        question = QuestionMCQ(
            {"question": "What is 1+1?", "options": ["1", "2"], "correct_answer": "b)"}
        )
        assert question.to_dict() == {
            "question_type": "MCQ",
            "question": "What is 1+1?",
            "options": ["1", "2"],
            "correct_answer": 1,
        }


class TestQuestionShortAnswer:
    """
    A group of tests that test QuestionShortAnswer
    """

    def test_construction(self):
        """
        Test construction of QuestionShortAnswer
        """
        question = QuestionShortAnswer(
            {"question": "What is your name?", "sample_answer": "My name is John."}
        )
        assert question.question_type == "Short Answer"
        assert question.question == "What is your name?"
        assert question.sample_answer == "My name is John."
        with pytest.raises(OutputFormatError):
            QuestionShortAnswer({})

    def test_to_dict(self):
        """
        Test to_dict method
        """
        question = QuestionShortAnswer(
            {"question": "What is your name?", "sample_answer": "My name is John."}
        )
        assert question.to_dict() == {
            "question_type": "Short Answer",
            "question": "What is your name?",
            "sample_answer": "My name is John.",
        }


class TestQuestionLongAnswer:
    """
    A group of tests that test QuestionLongAnswer
    """

    def test_construction(self):
        """
        Test construction of QuestionLongAnswer
        """
        question = QuestionLongAnswer(
            {"question": "What is your name?", "sample_answer": "My name is John."}
        )
        assert question.question_type == "Long Answer"
        assert question.question == "What is your name?"
        assert question.sample_answer == "My name is John."
        with pytest.raises(OutputFormatError):
            QuestionSubjectiveAnswer({})

    def test_to_dict(self):
        """
        Test to_dict method
        """
        question = QuestionLongAnswer(
            {"question": "What is your name?", "sample_answer": "My name is John."}
        )
        assert question.to_dict() == {
            "question_type": "Long Answer",
            "question": "What is your name?",
            "sample_answer": "My name is John.",
        }


class TestAssessment:
    """
    A group of tests that test Assessment.
    This does not test every method of Assessment, because we don't want to
    do LLM or DB calls while testing.
    """

    questions = [
        QuestionLongAnswer(
            {
                "question": "What is your name?",
                "sample_answer": "My name is John.",
            }
        ),
        QuestionShortAnswer(
            {"question": "How are you?", "sample_answer": "I am fine."}
        ),
        QuestionMCQ(
            {"question": "What is 1+1?", "options": ["1", "2"], "correct_answer": "b)"}
        ),
    ]

    def test_construction_questions(self):
        """
        Test construction of Assessment
        """

        assessment = Assessment(questions=self.questions)
        assert assessment.questions == self.questions
        assert assessment._id is None
        assert assessment.user_input is None
        assert assessment.last_modified and isinstance(assessment.last_modified, str)

    def test_construction_with_user_input_to_and_from_dict(self):
        """
        Test from_list and to_list are consistent with each other
        """
        user_input = {
            "topic": "Chemistry",
            "question_type": "SA",
            "num_questions": 10,
            "pdfs": ["chemistry.pdf", "organic.pdf"],
            "context_keywords": "molecules, reactions",
        }

        questions = [i.to_dict() for i in self.questions]
        assessment_dict = Assessment(
            user_input=user_input, questions=questions
        ).to_dict()
        assert assessment_dict["questions"] == questions
        assert assessment_dict["user_input"] == UserInput(**user_input).to_dict()
        assert assessment_dict["last_modified"] and isinstance(
            assessment_dict["last_modified"], str
        )

    def test_construction_from_str(self):
        """
        Test from_str method
        """
        assessment = Assessment(
            questions="""
            [
                {
                    "question_type": "Long Answer",
                    "question": "What is your name?",
                    "sample_answer": "My name is John.",
                },
                {
                    "question_type": "Short Answer",
                    "question": "How are you?",
                    "sample_answer": "I am fine.",
                },
                {
                    "question_type": "MCQ",
                    "question": "What is 1+1?",
                    "options": ["1", "2"],
                    "correct_answer": 1,
                },
            ]
            """
        )
        assert len(assessment.questions) == 3
        for left, right in zip(assessment.questions, self.questions):
            assert left.to_dict() == right.to_dict()


if __name__ == "__main__":
    pytest.main()
