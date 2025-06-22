from agents.market_search._query_generator import generate_search_queries
from agents.market_search._ddg_search import search_ddg
from agents.market_search._github_search import search_github
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    name="market-search",
    description="Searches market for products similar to a given idea.",
    version="1.0.0",
)

@mcp.tool()
def run_market_search(parsed_idea: dict, max_results=5) -> list:
    queries = generate_search_queries(parsed_idea)

    all_results = []
    for query in queries:
        # all_results.extend(search_ddg(query, max_results=max_results))
        all_results.extend(search_github(query, max_results=max_results))
    
    return all_results

# Entry point
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(mcp.sse_app(), host="0.0.0.0", port=8005)