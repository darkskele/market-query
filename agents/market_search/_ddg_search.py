from duckduckgo_search import DDGS
import time
import random

def search_ddg(query: str, max_results=5) -> list:
    results = []
    max_attempts = 5

    for attempt in range(max_attempts):
        try:
            with DDGS() as ddgs:
                for r in ddgs.text(query, max_results=max_results):
                    results.append({
                        "source": "ddg",
                        "title": r.get("title"),
                        "url": r.get("href"),
                        "snippet": (r.get("body")[:200] + '...') if r.get("body") and len(r.get("body")) > 200 else r.get("body"),
                        "metadata": {}
                    })
            break  # success, exit retry loop

        except Exception as e:
            wait = (2 ** attempt) + random.uniform(0.5, 1.5)
            print(f"🟡 DDG search failed: {e}. Retrying in {wait:.1f}s...")
            time.sleep(wait)

    return results
