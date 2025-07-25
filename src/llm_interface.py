"""
This file defines the 'get_prompt_response' function that is responsible
for sending a prompt string to the LLM and getting the response as a string
"""

import requests

from configs import API_TOKEN, API_URL, LLM_TIMEOUT
from exceptions import OutputFormatError


def get_prompt_response(prompt: str):
    """
    Function to get response from LLM
    """
    payload = {
        "inputs": f"[INST]{prompt}[/INST]",
        "parameters": {"return_full_text": False, "max_new_tokens": 10000},
    }

    try:
        response = requests.post(
            API_URL,
            headers={"Authorization": f"Bearer {API_TOKEN}"},
            json=payload,
            timeout=LLM_TIMEOUT,
        )
    except requests.RequestException:
        raise OutputFormatError("Could not get LLM response") from None

    try:
        ret = response.json()[0]["generated_text"]
    except (IndexError, KeyError, ValueError):
        raise OutputFormatError("LLM sent an invalid 'generated_text'") from None

    if not isinstance(ret, str):
        raise OutputFormatError(
            "LLM sent an invalid 'generated_text', must be string"
        ) from None

    return ret
