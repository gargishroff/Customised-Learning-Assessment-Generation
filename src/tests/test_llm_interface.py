"""
pytest based unit testing for everything in llm_interface.py
"""

import pytest

from llm_interface import get_prompt_response


class TestGetPromptResponse:
    """
    Tests get_prompt_response function
    """

    def test_simple_cases(self):
        """
        Test that LLM gives some string response
        """
        assert isinstance(get_prompt_response("Hello, how are you"), str)


if __name__ == "__main__":
    pytest.main()
