"""
Implements UserInput class
"""

import json
from typing import Any

import textract

from configs import UPLOADS_BASE
from exceptions import UserInputError


PROMPT_TEMPLATE_MCQ = """
Generate {} MCQ style assessment questions on the topic '{}'. {}

The output must be a very compact one-line JSON list of all questions as a dict.
Each dict must have attributes 'question', 'options' and 'correct_answer'
(which should be an index into 'options').
Additionally, the dict must have an attribute 'question_type' with value 'MCQ'.
{}
"""

PROMPT_TEMPLATE_SUBJECTIVE = """
Generate {} {} style assessment questions on the topic '{}'. {}

The output must be a very compact one-line JSON list of all questions as a dict.
Each dict must have attributes 'question' and 'sample_answer'.
Additionally, the dict must have an attribute 'question_type' with value '{}'.
{}
"""


class UserInput:
    """
    A class that stores user input from page 1.
    Has methods to manage and process the input.
    """

    def __init__(
        self,
        topic: str,
        question_type: str,
        num_questions: int,
        pdfs: list[str],
        context_keywords: str = "",
    ):
        if not isinstance(topic, str):
            raise UserInputError("'topic' must be str")

        self.topic = topic.strip()
        if not isinstance(question_type, str):
            raise UserInputError("'question_type' must be str")

        self.question_type = question_type.lower()
        if self.question_type == "la":
            self.question_type = "Long Answer"

        if self.question_type == "sa":
            self.question_type = "Short Answer"

        if not isinstance(num_questions, int):
            raise UserInputError("'num_questions' must be int")

        self.num_questions = num_questions
        if not isinstance(context_keywords, str):
            raise UserInputError("'context_keywords' must be str")

        self.context_keywords = context_keywords.strip()
        if not isinstance(pdfs, list):
            raise UserInputError("'pdfs' must be list")

        for i in pdfs:
            if not isinstance(i, str):
                raise UserInputError("'pdfs' must be list of strings")

        self.pdfs = pdfs

    @classmethod
    def from_request_form(cls, request_form: dict[str, Any]):
        """
        Constructor to make UserInput instance from request.json style object
        """
        if not isinstance(request_form, dict):
            raise UserInputError("request_form must be a dictionary")

        try:
            pdfs = json.loads(request_form["pdfs"])
        except (KeyError, json.JSONDecodeError):
            pdfs = {"fileList": []}

        try:
            return cls(
                request_form["topic"],
                request_form["question_type"],
                int(request_form["num_questions"]),
                [i["name"] for i in pdfs["fileList"]],
                request_form.get("context_keywords", ""),
            )
        except KeyError:
            raise UserInputError("Missing form field") from None

        except (ValueError, TypeError):
            raise UserInputError("Incorrect form field type") from None

    def make_prompt(self):
        """
        Make a prompt that is sent to the LLM
        """
        context_keywords = (
            f"Try to inculcate the following context: {self.context_keywords}"
            if self.context_keywords
            else ""
        )

        pdf_text = ""
        if self.pdfs:
            processed = textract.process(UPLOADS_BASE / self.pdfs[0]).decode()
            if processed:
                pdf_text = f"Here is some additional context on the topic: {processed}"

        if "mcq" in self.question_type:
            return PROMPT_TEMPLATE_MCQ.format(
                self.num_questions, self.topic, context_keywords, pdf_text
            )

        return PROMPT_TEMPLATE_SUBJECTIVE.format(
            self.num_questions,
            self.question_type,
            self.topic,
            context_keywords,
            self.question_type,
            pdf_text,
        )

    def to_dict(self):
        """
        Returns dict representation of UserInput object
        """
        return {
            "topic": self.topic,
            "question_type": self.question_type,
            "num_questions": self.num_questions,
            "context_keywords": self.context_keywords,
            "pdfs": self.pdfs,
        }


if __name__ == "__main__":
    # test code
    user_input = UserInput("Thermodynamics", "MCQ", 10, [])
    print(user_input.make_prompt())
