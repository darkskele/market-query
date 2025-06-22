import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from mcp.server.fastmcp import FastMCP

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

mcp = FastMCP(
    name="startup-similarity-scorer",
    description="Scores startup ideas in terms of similarity to user idea.",
    version="1.0.0",
)

@mcp.tool()
def score_similarity(parsed_idea: dict, market_results: list, model="gpt-4") -> dict:
    scored_results = []

    for result in market_results:
        prompt = f"""
Compare the following startup idea to an existing product. Return ONLY a valid JSON object with the keys:
- similarity (float from 0.0 to 1.0)
- comment (brief comparison)

Startup Idea:
Description: {parsed_idea.get("description")}
Tags: {', '.join(parsed_idea.get("tags", []))}
Target user: {parsed_idea.get("target_user")}
Core features: {', '.join(parsed_idea.get("core_features", []))}
Use case: {parsed_idea.get("use_case")}

Market Result:
Title: {result.get("title")}
Description: {result.get("snippet")}

Return a JSON object. No markdown.
"""

        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            text = response.choices[0].message.content
            json_start = text.index('{')
            scored = json.loads(text[json_start:])
            result["similarity"] = scored.get("similarity", 0.0)
            result["comment"] = scored.get("comment", "")
        except Exception as e:
            print(f"❌ Failed to score: {result.get('title')}")
            print("Error:", e)
            result["similarity"] = 0.0
            result["comment"] = "Scoring failed"

        scored_results.append(result)

    # Aggregate uniqueness and saturation
    similarities = [r["similarity"] for r in scored_results]
    max_sim = max(similarities, default=0.0)
    avg_sim = sum(similarities) / len(similarities) if similarities else 0.0

    uniqueness_score = round((1 - max_sim) * (1 - avg_sim), 2)
    saturation_label = (
        "High market saturation" if avg_sim > 0.65 else
        "Moderate market saturation" if avg_sim > 0.35 else
        "Low market saturation"
    )

    return {
        "scored_results": scored_results,
        "uniqueness_score": round(uniqueness_score, 2),
        "saturation": saturation_label
    }

# Entry point
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(mcp.sse_app(), host="0.0.0.0", port=8002)