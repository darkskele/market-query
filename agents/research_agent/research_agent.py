#!/usr/bin/env python3
"""
Research Agent MCP CLIENT - Uses the ArXiv MCP server
This is the CLIENT that connects to the server and uses its tools
Run this SECOND: python research_client.py (after server is running)
"""

import asyncio
import json
import os
from dotenv import load_dotenv
from anthropic import Anthropic

# MCP client imports
from fastmcp import Client
from fastmcp.client.transports import SSETransport

# Load environment
load_dotenv()

class ResearchAgentClient:
    """Research Agent CLIENT that connects to the ArXiv MCP server"""
    
    def __init__(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("Please set ANTHROPIC_API_KEY environment variable")
        
        self.anthropic = Anthropic(api_key=api_key)
        self.server_url = "http://localhost:8001/sse"  # Connect to server
    
    async def get_server_info_via_server(self):
        """Get server information via MCP"""
        print("🤖 CLIENT: Requesting server info...")
        
        transport = SSETransport(self.server_url)
        async with Client(transport) as client:
            result = await client.call_tool(
                name="get_server_info",
                arguments={}
            )
            
            # Fix: Extract JSON from TextContent object
            if result and hasattr(result[0], 'text'):
                # Parse the JSON string from the text content
                try:
                    return json.loads(result[0].text)
                except json.JSONDecodeError:
                    return {"error": "Could not parse server response"}
            elif result:
                return result
            else:
                return {"error": "No response from server"}
    
    async def search_papers_via_server(self, query: str, max_results: int = 5):
        """Use the MCP server to search for papers"""
        print(f"🤖 CLIENT: Requesting search for '{query}' from server...")
        
        transport = SSETransport(self.server_url)
        async with Client(transport) as client:
            # Call the server's search tool
            result = await client.call_tool(
                name="search_arxiv_papers",
                arguments={"query": query, "max_results": max_results}
            )
            
            # Fix: Extract JSON from TextContent object
            if result and hasattr(result[0], 'text'):
                try:
                    return json.loads(result[0].text)
                except json.JSONDecodeError:
                    return {"error": "Could not parse server response"}
            elif result:
                return result
            else:
                return {"error": "No response from server"}
    
    async def demo_client_server_interaction(self):
        """Demonstrate how client and server interact"""
        print("\n🎯 RESEARCH AGENT CLIENT DEMO")
        print("=" * 60)
        print("🔄 This CLIENT connects TO the MCP server")
        print("🛠️ The CLIENT uses tools PROVIDED BY the server")
        print("=" * 60)
        
        try:
            # Test 1: Get server info
            print("\n1️⃣ CLIENT → SERVER: Getting server capabilities...")
            server_info = await self.get_server_info_via_server()
            
            if isinstance(server_info, dict) and not server_info.get("error"):
                print(f"✅ CLIENT ← SERVER: {server_info.get('server_name')}")
                print(f"🔧 Available tools: {', '.join(server_info.get('capabilities', []))}")
            else:
                print(f"❌ SERVER response: {server_info}")
                return
            
            # Test 2: Search papers via server
            queries = [
                "quantum machine learning",
                "transformer attention mechanisms",
                "climate change AI"
            ]
            
            for i, query in enumerate(queries, 2):
                print(f"\n{i}️⃣ CLIENT → SERVER: Search request for '{query}'")
                
                papers = await self.search_papers_via_server(query, 3)
                
                if isinstance(papers, dict) and papers.get("error"):
                    print(f"❌ CLIENT ← SERVER: Error - {papers['error']}")
                    continue
                
                # Parse if it's a JSON string
                if isinstance(papers, str):
                    try:
                        papers = json.loads(papers)
                    except:
                        print(f"❌ CLIENT: Could not parse server response")
                        continue
                
                print(f"✅ CLIENT ← SERVER: Found {papers.get('total_found', 0)} papers")
                
                # Show results - Fix: Show all papers, not just first 2
                for j, paper in enumerate(papers.get("papers", []), 1):
                    print(f"   📄 Paper {j}: {paper['title'][:50]}...")
                    print(f"      👥 Authors: {', '.join(paper['authors'][:2])}")
                
                # AI analysis of server results
                if papers.get("papers"):
                    print(f"\n🧠 CLIENT: Running AI analysis on server data...")
                    
                    paper_titles = [p['title'] for p in papers['papers'][:3]]
                    analysis_prompt = f"""Analyze these research papers about "{query}":

{chr(10).join(f'- {title}' for title in paper_titles)}

Provide a brief insight on the main research direction (1-2 sentences)."""
                    
                    try:
                        response = await asyncio.to_thread(
                            self.anthropic.messages.create,
                            model="claude-3-5-haiku-20241022",
                            max_tokens=150,
                            messages=[{"role": "user", "content": analysis_prompt}]
                        )
                        
                        print(f"💡 CLIENT AI Analysis: {response.content[0].text}")
                        
                    except Exception as e:
                        print(f"❌ CLIENT AI analysis failed: {e}")
                
                if i < len(queries) + 1:
                    print("\n⏳ CLIENT: Preparing next request to server...")
                    await asyncio.sleep(1)
            
            print("\n🎉 CLIENT-SERVER INTERACTION COMPLETE!")
            print("\n💡 What happened:")
            print("   1️⃣ CLIENT connected to MCP SERVER")
            print("   2️⃣ CLIENT used SERVER's research tools")
            print("   3️⃣ SERVER processed requests and returned data")
            print("   4️⃣ CLIENT performed AI analysis on SERVER data")
            print("   5️⃣ This is the foundation for multi-agent coordination!")
            
        except Exception as e:
            print(f"❌ CLIENT demo failed: {e}")
            print("💡 Make sure the server is running: python arxiv_server.py")

async def main():
    print("🤖 RESEARCH AGENT CLIENT")
    print("📋 This CLIENT will:")
    print("   • Connect to the ArXiv MCP SERVER")
    print("   • Use the server's research tools")
    print("   • Demonstrate client-server coordination")
    print("   • Run AI analysis on server data")
    print()
    print("⚠️  IMPORTANT: Make sure the SERVER is running first!")
    print("   Terminal 1: python arxiv_server.py")
    print("   Terminal 2: python research_client.py (this file)")
    print()
    
    try:
        client = ResearchAgentClient()
        await client.demo_client_server_interaction()
        
    except ValueError as e:
        print(f"❌ Setup error: {e}")
        print("💡 Set your API key: export ANTHROPIC_API_KEY=your_key_here")
    except Exception as e:
        print(f"❌ Client error: {e}")

if __name__ == "__main__":
    asyncio.run(main())