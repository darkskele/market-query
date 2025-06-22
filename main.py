"""
main.py — Entry point for running the NANDA MVP flow.

This script takes a startup idea (via CLI arg or input prompt),
runs it through a series of agents defined in `flows/mvp.yaml`,
and prints out the final similarity scoring results in JSON format.

Usage:
    python main.py "An AI tool for pricing freelance services"
"""

from mcp_runner import run_flow
import sys
import json

def main():
    # Get startup idea from command-line arguments or interactive input
    if len(sys.argv) > 1:
        idea = " ".join(sys.argv[1:])  # Handle multi-word ideas
    else:
        idea = input("💡 Enter your startup idea: ").strip()

    # Run the full agent chain using the YAML-defined flow
    result = run_flow("flows/mvp.yaml", {"idea_text": idea}) 

    # Print only the final similarity scoring output as formatted JSON
    print(json.dumps(result["score"]["output"], indent=2))

if __name__ == "__main__":
    main()
