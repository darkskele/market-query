"""
Anthropic-powered summarizer for market analysis results
"""
import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

def summarize_market_analysis(analysis_result: dict) -> str:
    """
    Use Anthropic Claude to create an executive summary of market analysis results
    """
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    # Extract key data
    uniqueness_score = analysis_result.get("uniqueness_score", 0)
    saturation = analysis_result.get("saturation", "Unknown")
    gap_analysis = analysis_result.get("gap_analysis", {})
    scored_results = analysis_result.get("scored_results", [])
    
    prompt = f"""
    Analyze this startup market research and provide a concise executive summary:
    
    **Market Analysis Results:**
    - Uniqueness Score: {uniqueness_score}/1.0
    - Market Saturation: {saturation}
    - Gap Analysis: {gap_analysis}
    
    **Competitors Found:**
    {len(scored_results)} competitors analyzed
    
    **Top Competitors:**
    {chr(10).join([f"- {comp.get('title', 'Unknown')}: {comp.get('similarity', 0):.2f} similarity" for comp in scored_results[:3]])}
    
    Provide a structured executive summary with:
    1. 🎯 **Market Opportunity** (2-3 sentences)
    2. ⚠️ **Key Risks** (1-2 sentences) 
    3. 💡 **Strategic Recommendation** (1-2 sentences)
    4. 📊 **Confidence Level** (High/Medium/Low with brief reason)
    
    Keep it concise and actionable for entrepreneurs. Use markdown formatting.
    """
    
    try:
        response = client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=600,
            temperature=0.3,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    
    except Exception as e:
        return f"❌ Summary generation failed: {str(e)}"

# Fallback function for when AI summary fails
def create_basic_summary(analysis_result: dict) -> str:
    """
    Create a basic summary without AI when API fails
    """
    uniqueness_score = analysis_result.get("uniqueness_score", 0)
    scored_results = analysis_result.get("scored_results", [])
    avg_similarity = sum(r.get("similarity", 0) for r in scored_results) / len(scored_results) if scored_results else 0
    
    # Determine market opportunity
    if uniqueness_score > 0.7:
        opportunity = "🎯 **High Market Opportunity**: Your idea shows strong uniqueness with limited direct competition."
    elif uniqueness_score > 0.4:
        opportunity = "🎯 **Moderate Market Opportunity**: Your idea has some unique aspects but faces moderate competition."
    else:
        opportunity = "🎯 **Challenging Market**: Your idea faces significant competition in a crowded market."
    
    # Determine risks
    if avg_similarity > 0.7:
        risks = "⚠️ **High Risk**: Multiple competitors with very similar offerings detected."
    elif avg_similarity > 0.4:
        risks = "⚠️ **Moderate Risk**: Some similar competitors exist but differentiation is possible."
    else:
        risks = "⚠️ **Low Risk**: Few direct competitors found, but market validation needed."
    
    # Strategic recommendation
    if uniqueness_score > 0.6 and avg_similarity < 0.5:
        strategy = "💡 **Recommended Strategy**: Focus on unique features and rapid market entry."
    else:
        strategy = "💡 **Recommended Strategy**: Emphasize differentiation and identify specific market niches."
    
    # Confidence level
    competitor_count = len(scored_results)
    if competitor_count >= 5:
        confidence = "📊 **Confidence Level**: High - Based on comprehensive competitor analysis"
    elif competitor_count >= 2:
        confidence = "📊 **Confidence Level**: Medium - Based on moderate competitor data"
    else:
        confidence = "📊 **Confidence Level**: Low - Limited competitor data available"
    
    return f"""
{opportunity}

{risks}

{strategy}

{confidence}
    """.strip()