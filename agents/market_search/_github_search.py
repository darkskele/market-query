import os
import requests

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

def search_github(query: str, max_results=5) -> list:
    url = "https://api.github.com/search/repositories"
    params = {
        "q": query,
        "sort": "stars",
        "order": "desc",
        "per_page": max_results
    }

    response = requests.get(url, headers=HEADERS, params=params)
    if response.status_code != 200:
        print(f"GitHub API error: {response.status_code} – {response.text}")
        return []

    data = response.json()
    results = []
    for repo in data.get("items", []):
        results.append({
            "source": "github",
            "title": repo.get("name"),
            "url": repo.get("html_url"),
            "snippet": (repo.get("description")[:200] + '...') if repo.get("description") and len(repo.get("description")) > 200 else (repo.get("description") or ""),
            "metadata": {
                "stars": repo.get("stargazers_count"),
                "language": repo.get("language"),
                "owner": repo.get("owner", {}).get("login"),
            }
        })
    return results
