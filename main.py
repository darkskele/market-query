"""
main.py — Entry point for running the NANDA MVP flow with AI summarization.
"""

from mcp_runner import run_flow
from agents.summarizer import summarize_market_analysis
import sys
import json

def main():
    # Get startup idea from command-line arguments or interactive input
    if len(sys.argv) > 1:
        idea = " ".join(sys.argv[1:])
    else:
        idea = input("💡 Enter your startup idea: ").strip()

    print(f"\n🔍 Analyzing: '{idea}'")
    print("=" * 60)
    
    # Run the full agent chain
    result = run_flow("flows/mvp.yaml", {"idea_text": idea})
    
    # Get the final scoring results 
    final_results = result.get("score", {}).get("output", {})
    
    # Generate AI summary
    print("\n🤖 AI Executive Summary:")
    print("-" * 40)
    summary = summarize_market_analysis(final_results)
    print(summary)
    
    # Option to see full JSON
    show_details = input("\n📋 Show detailed JSON results? (y/n): ").lower().startswith('y')
    if show_details:
        print("\n📊 Detailed Analysis:")
        print("=" * 60)
        print(json.dumps(final_results, indent=2))

if __name__ == "__main__":
    main()
