import json
from openai import OpenAI

client = OpenAI()

def generate_search_queries(parsed_idea: dict, n: int = 3) -> list:
    system_msg = "You generate concise search queries for product or competitor discovery."
    user_msg = f"""
Given the startup idea:

Description: {parsed_idea.get("description")}
Tags: {', '.join(parsed_idea.get("tags", []))}
Core features: {', '.join(parsed_idea.get("core_features", []))}
Target user: {parsed_idea.get("target_user")}

Suggest {n} concise search engine queries (5–10 words each) to find existing products or competitors. Return as a JSON Python list of strings.
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg}
        ],
        temperature=0.3
    )

    result = response.choices[0].message.content
    try:
        json_start = result.index('[')
        return json.loads(result[json_start:])
    except Exception:
        print("Couldn’t parse queries. Raw output:\n", result)
        return []
