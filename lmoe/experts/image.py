from lmoe.api.model_expert import ModelExpert
from lmoe.api.lmoe_query import LmoeQuery
from lmoe.framework.expert_registry import expert

import base64
import binascii
import ollama
import re
import requests


def extract_base64(input_string):
    """Extract base64 from text which may include whitespace or non-base64 data."""
    # Use regular expression to extract Base64 data
    match = re.search(r"\s*(user_context:)?\s*([A-Za-z0-9+/]+={0,2})", input_string)
    if match:
        base64_data = match.group(2)
        # Remove whitespace and padding characters
        base64_data = base64_data.replace(r"[A-Za-z0-9+/=]", "")
        # Add padding if necessary
        while len(base64_data) % 4 != 0:
            base64_data += "="
        return base64_data
    else:
        return None


def check_base64(s):
    """Verifies that a base64 string is valid."""
    try:
        if not s.isascii():
            print("s is not ascii")
            return False
        decoded_bytes = base64.standard_b64decode(s)
        decoded_string = base64.standard_b64encode(decoded_bytes)
        return True
    except Exception as e:
        print(e)
        return False


@expert
class Image(ModelExpert):

    @classmethod
    def name(cls):
        return "IMAGE"

    def description(self):
        return "Analyzes the contents of images and answers questions about them."

    def example_queries(self):
        return [
            "what's in this picture",
            "what's in this iamge",
            "how many people are in this picture",
            "where was this picture taken",
        ]

    def generate(self, lmoe_query: LmoeQuery):
        # TODO: Have a good way to get image context (interpret base64 context, then just from filename)
        extracted_base64 = extract_base64(lmoe_query.stdin_context)
        if not check_base64(extracted_base64):
            print("bad base64")
            exit(1)

        # TODO: Ollama client for this is not working but raw HTTP calls are currently. Open a bug.
        # TODO: replace with a more general ollama client allowing configuration?
        # TODO: extract JSON, support streaming
        try:
            response = requests.post(
                "http://127.0.0.1:11434/api/generate",
                json={
                    "model": "llava",
                    "prompt": lmoe_query.user_query,
                    "stream": False,
                    "images": [extracted_base64],
                },
            )
            print(response.text)
        except requests.RequestException as e:
            print("Error:", e)
