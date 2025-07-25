"""
Implements the Assessment class
"""

import re
import string

from datetime import datetime
from typing import Any

# This third party library is used instead of stdlib json is because it accepts
# trailing commas in json - something that the LLM can incorrectly add
import jsonc

from bson.objectid import ObjectId

import configs
from exceptions import DBError, OutputFormatError, UserInputError
from llm_interface import get_prompt_response
from userinput import UserInput


def option_id_as_int(option_id: str | int):
    """
    Helper function to normalize option id to an int
    """
    if isinstance(option_id, int):
        return option_id

    if not isinstance(option_id, str):
        raise OutputFormatError("Invalid option id type")

    option_id = option_id.strip().rstrip(".").rstrip(")").lower()
    if len(option_id) != 1:
        raise OutputFormatError("Invalid option id value")

    try:
        return int(option_id)
    except ValueError:
        try:
            return string.ascii_lowercase.index(option_id)
        except ValueError:
            raise OutputFormatError("Invalid option id value") from None


class QuestionBase:
    """
    A base class for implementing different kind of questions.
    This represents the simplest kind of question.
    """

    question_type = None

    def __init__(self, question_dict: dict[str, Any]):
        if not isinstance(question_dict, dict):
            raise OutputFormatError("'question_dict' must be a dictionary")

        try:
            self.update_question(question_dict["question"])
        except KeyError:
            raise OutputFormatError(
                "'question_dict' must have key 'question'"
            ) from None

    def __str__(self):
        return self.question

    def update_question(self, question: str):
        """
        Method to update the question
        """
        if not isinstance(question, str):
            raise OutputFormatError("'question' must be a str object")

        self.question = question

    def to_dict(self) -> dict[str, Any]:
        """
        Generates a dictionary representation of the question that can be
        passed to the frontend
        """
        if self.question_type is None:
            raise RuntimeError(
                "Cannot convert a baseclass question type into a dictionary"
            )

        return {"question_type": self.question_type, "question": self.question}


class QuestionSubjectiveAnswer(QuestionBase):
    """
    A class for representing subjective answer kind of questions
    """

    def __init__(self, question_dict: dict[str, Any]):
        super().__init__(question_dict)
        try:
            self.update_sample_answer(question_dict["sample_answer"])
        except KeyError:
            raise OutputFormatError(
                "'question_dict' must have key 'sample_answer'"
            ) from None

    def __str__(self):
        return f"{self.question}\nSample Answer: {self.sample_answer}"

    def update_sample_answer(self, sample_answer: str):
        """
        Method to update the sample_answer
        """
        if not isinstance(sample_answer, str):
            raise OutputFormatError("'sample_answer' must be a str object")

        self.sample_answer = sample_answer

    def to_dict(self):
        ret = super().to_dict()
        ret["sample_answer"] = self.sample_answer
        return ret


class QuestionShortAnswer(QuestionSubjectiveAnswer):
    """
    A class for representing short answer kind of questions
    """

    question_type = "Short Answer"


class QuestionLongAnswer(QuestionSubjectiveAnswer):
    """
    A class for representing long answer kind of questions
    """

    question_type = "Long Answer"


class QuestionMCQ(QuestionBase):
    """
    A class for representing MCQ kind of questions
    """

    question_type = "MCQ"

    def __init__(self, question_dict: dict[str, Any]):
        super().__init__(question_dict)
        self.options: list[str] = []
        try:
            for i, option in enumerate(question_dict["options"]):
                self.update_option(i, option)
        except KeyError:
            raise OutputFormatError("'question_dict' must have key 'options'") from None

        try:
            self.update_correct_answer(question_dict["correct_answer"])
        except KeyError:
            raise OutputFormatError(
                "'question_dict' must have key 'correct_answer'"
            ) from None

    def __str__(self):
        ret = f"{self.question}\nOptions:\n"
        for i, val in enumerate(self.options):
            ret += f"({i + 1}) {val}"
            if i == self.correct_answer:
                ret += " (correct answer)"
            ret += "\n"

        return ret

    def update_correct_answer(self, correct_answer: int | str):
        """
        Updates the correct answer
        """
        self.correct_answer = option_id_as_int(correct_answer)
        if not 0 <= self.correct_answer < len(self.options):
            raise OutputFormatError("'correct_answer' value must be in options")

    def update_option(self, index: int | str, option: str):
        """
        Function to update an option in a question
        """
        if not isinstance(option, str):
            raise OutputFormatError("'option' must be a string")

        index = option_id_as_int(index)
        if 0 <= index < len(self.options):
            self.options[index] = option
        elif index == len(self.options):
            self.options.append(option)
        else:
            raise OutputFormatError("'index' out of range")

    def to_dict(self):
        ret = super().to_dict()
        ret["options"] = self.options
        ret["correct_answer"] = self.correct_answer
        return ret


def _make_question_obj(question: dict[str, Any] | QuestionBase):
    """
    Internal helper function called to ensure every question dict is converted
    to equivalent Question class.
    """
    if isinstance(question, QuestionBase):
        return question

    if not isinstance(question, dict):
        raise OutputFormatError("question must be a dict")

    try:
        q_type = question["question_type"].lower()
        if "mcq" in q_type:
            return QuestionMCQ(question)

        if "short" in q_type:
            return QuestionShortAnswer(question)

        if "long" in q_type:
            return QuestionLongAnswer(question)

        raise OutputFormatError("Invalid question type recieved")

    except KeyError:
        raise OutputFormatError(
            "All questions must have the 'question_type' attribute"
        ) from None


def _questions_from_str_or_none(content: str | None):
    """
    Internal helper function called to get a list of question dicts from str
    output generated by the LLM
    """
    questions: list[dict[str, Any]] = []
    if content:
        try:
            for match in re.findall(r"```json(.*?)```", content, re.DOTALL):
                if isinstance(match, str):
                    questions.extend(jsonc.loads(match.strip()))

            if not questions:
                questions.extend(jsonc.loads(content.strip()))

        except jsonc.JSONDecodeError:
            raise OutputFormatError("LLM sent invalid json response") from None

    return questions


class Assessment:
    """
    Assessment class
    """

    def __init__(
        self,
        _id: ObjectId | dict[str, str] | None = None,
        user_input: UserInput | dict | None = None,
        questions: list[QuestionBase] | list[dict[str, Any]] | str | None = None,
        last_modified: str | None = None,
    ):
        if isinstance(_id, dict):
            _id = ObjectId(_id["$oid"])

        self._id = _id
        self.user_input = (
            UserInput(**user_input) if isinstance(user_input, dict) else user_input
        )
        if questions is None or isinstance(questions, str):
            questions = _questions_from_str_or_none(questions)
        self.questions = [_make_question_obj(i) for i in questions]

        self.last_modified = (
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if last_modified is None
            else last_modified
        )

    def __str__(self):
        return "\n\n".join(f"{i}. {val}" for i, val in enumerate(self.questions))

    @classmethod
    def from_user_input(cls, user_input: UserInput):
        """
        Constructs Assessment object from given UserInput object
        """
        return cls(
            user_input=user_input,
            questions=get_prompt_response(user_input.make_prompt()),
        )

    @classmethod
    def from_db(cls, assessment_id: ObjectId):
        """
        Constructs Assessment by fetching the corresponding record in the db
        """
        if configs.pymongo is None or configs.pymongo.db is None:
            raise DBError()

        return cls(**configs.pymongo.db.assessments.find_one_or_404(assessment_id))

    @staticmethod
    def delete_from_db(assessment_id: ObjectId):
        """
        Delete the corresponding assessment from the DB
        """
        if configs.pymongo is None or configs.pymongo.db is None:
            raise DBError()

        result = configs.pymongo.db.assessments.delete_one({"_id": assessment_id})

        if result.deleted_count == 0:
            raise UserInputError("Assessment not found or already deleted.")

        return result.deleted_count

    @classmethod
    def from_request_json(cls, request_json: Any):
        """
        Constructor to make Assessment instance from request.json style object
        """
        if not isinstance(request_json, dict):
            raise UserInputError("request_json must be a dictionary")

        try:
            return cls(
                _id=request_json.get("_id"),
                user_input=request_json["user_input"],
                questions=request_json["questions"],
            )
        except KeyError:
            raise UserInputError("'request_json' missing needed attributes!") from None

    def to_dict(self, with_id: bool = True):
        """
        Returns the dict representation of the Assessment instance.
        This method needs 'user_input' to be set already.

        The argument with_id controls if the _id attribute is included in the
        returned dictionary.
        """

        if self.user_input is None:
            raise RuntimeError("'user_input' unset")

        ret = {
            "user_input": self.user_input.to_dict(),
            "questions": [i.to_dict() for i in self.questions],
            "last_modified": self.last_modified,
        }

        if with_id:
            ret["_id"] = self._id

        return ret

    def save(self):
        """
        This method saves the current instance as a new entry in the db.
        Sets a new object ID
        """
        if configs.pymongo is None or configs.pymongo.db is None:
            raise DBError()

        if self._id is None:
            result = configs.pymongo.db.assessments.insert_one(
                self.to_dict(with_id=False)
            )
            if not isinstance(result.inserted_id, ObjectId):
                raise DBError()

            self._id = result.inserted_id
        else:
            result = configs.pymongo.db.assessments.replace_one(
                {"_id": self._id}, self.to_dict(with_id=False)
            )

    def get_id(self):
        """
        This method gets the _id attribute if it is set, and errors otherwise
        """
        if self._id is None:
            raise RuntimeError("Cannot call 'get_id' when _id is unset")

        return self._id


def get_all_assessments():
    """
    Helper function to return a list of assessments as a dictionary, as stored
    in the database.
    """
    if configs.pymongo is None or configs.pymongo.db is None:
        raise DBError()

    return list(configs.pymongo.db.assessments.find())
