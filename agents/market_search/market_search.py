from agents.market_search._query_generator import generate_search_queries
from agents.market_search._ddg_search import search_ddg
from agents.market_search._github_search import search_github

def run_market_search(parsed_idea: dict, max_results=5) -> list:
    queries = generate_search_queries(parsed_idea)

    all_results = []
    for query in queries:
        all_results.extend(search_ddg(query, max_results=max_results))
        all_results.extend(search_github(query, max_results=max_results))
    
    return all_results

if __name__ == "__main__":
    example_idea = {
        "description": "An AI tool that helps freelancers price services using competitor data",
        "tags": ["AI", "freelancer", "pricing", "market analysis"],
        "core_features": ["real-time scraping", "competitor analysis", "dynamic pricing"],
        "target_user": "freelancers"
    }

    results = run_market_search(example_idea, max_results=3)

    for i, r in enumerate(results, 1):
        print(f"\nResult {i} ({r['source']})")
        print(f"{r['title']}")
        print(f"{r['url']}")
        print(f"{r['snippet'][:200]}") 
        if r['metadata']:
            print(f"Metadata: {r['metadata']}")