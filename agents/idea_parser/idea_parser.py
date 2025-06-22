"""
idea_parser.py — Extracts structured information from a freeform startup idea.

This agent uses OpenAI's chat completion API to parse a raw startup idea string
into a structured JSON format containing:
- description
- tags
- target_user
- core_features
- use_case

Example usage:
    parsed = parse_idea("An AI tool that helps freelancers price services using competitor data")
"""

import json
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env (specifically for OPENAI_API_KEY)
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def parse_idea(idea: str) -> dict:
    """
    Uses GPT to parse a startup idea string into a structured dictionary.

    Args:
        idea (str): The freeform user idea input.

    Returns:
        dict: Parsed fields (description, tags, target_user, core_features, use_case)
    """
    prompt = f"""
Extract the following fields from the startup idea and return a VALID JSON object with these keys:
- description
- tags (list of strings)
- target_user
- core_features (list of strings)
- use_case

Startup idea: \"\"\"{idea}\"\"\"

Only output a valid JSON object. No explanation, no markdown.
"""

    try:
        # Call OpenAI API with prompt
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        # Extract JSON content from raw response
        text = response.choices[0].message.content
        json_start = text.index('{')
        json_str = text[json_start:]
        return json.loads(json_str)

    except Exception as e:
        # Debug output if something goes wrong
        print("Failed to parse JSON. Raw output:")
        print(text if 'text' in locals() else "<No response>")
        print("Error:", e)
        return {}

if __name__ == "__main__":
    idea = "A platform that helps creators monetize AI-generated short-form video using local models on mobile."
    print(parse_idea(idea))
