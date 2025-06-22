#!/usr/bin/env python3
"""
Enhanced Gap Detection MCP Server - Analyzes market data for research gaps
Processes scored results from multiple sources to detect opportunities
Run on port 8002
"""

from fastmcp import FastMCP
from fastmcp.server.http import create_sse_app
import uvicorn
import json
from typing import Dict, Any, List
from datetime import datetime
import statistics
from collections import Counter

app = FastMCP("Enhanced Research Gap Detection Server")

# @app.tool()
def analyze_market_gaps(scored_results, uniqueness_score, saturation) -> Dict[str, Any]:
    """
    Analyze market gaps from scored results across multiple sources
    
    Args:
        market_data: JSON string containing scored_results, uniqueness_score, and saturation
        
    Expected input format:
    {
        "scored_results": [
            {
                "source": "ddg" | "github" | "academic",
                "title": "Product/repo title",
                "url": "Link to product/repo", 
                "snippet": "Description",
                "metadata": {"stars": 100, "language": "Python", ...},
                "similarity": 0.75,
                "comment": "LLM analysis of overlaps and gaps"
            }
        ],
        "uniqueness_score": 0.8,
        "saturation": "Low market saturation"
    }
    """
    try:
        
        # Perform comprehensive gap analysis
        analysis = _perform_comprehensive_gap_analysis(scored_results, uniqueness_score, saturation)
        
        return {
            "server_name": "Enhanced Research Gap Detection Server",
            "analysis_timestamp": datetime.now().isoformat(),
            "market_analysis": analysis,
            "recommendations": _generate_strategic_recommendations(analysis),
            "success": True
        }
        
    except Exception as e:
        return {
            "error": str(e),
            "success": False
        }

def _perform_comprehensive_gap_analysis(scored_results: List[Dict], uniqueness_score: float, saturation: str) -> Dict[str, Any]:
    """Perform detailed gap analysis on market data"""
    
    # Market landscape metrics
    market_metrics = _calculate_market_metrics(scored_results, uniqueness_score, saturation)
    
    # Identify specific gaps
    gaps_identified = _identify_market_gaps(scored_results, uniqueness_score, market_metrics)
    
    # Calculate opportunity scoring
    opportunity_score = _calculate_opportunity_score(uniqueness_score, market_metrics, saturation)
    
    # Determine market positioning strategy
    market_position = _determine_market_position(uniqueness_score, market_metrics)
    
    # Competitive landscape analysis
    competitive_analysis = _analyze_competitive_landscape(scored_results)
    
    return {
        "market_metrics": market_metrics,
        "gaps_identified": gaps_identified,
        "opportunity_score": opportunity_score,
        "market_position": market_position,
        "competitive_analysis": competitive_analysis
    }

def _calculate_market_metrics(scored_results: List[Dict], uniqueness_score: float, saturation: str) -> Dict[str, Any]:
    """Calculate comprehensive market metrics"""
    
    if not scored_results:
        return {
            "total_competitors": 0,
            "source_distribution": {},
            "similarity_stats": {"avg": 0, "max": 0, "min": 0, "std": 0},
            "uniqueness_score": uniqueness_score,
            "saturation_level": saturation
        }
    
    # Source distribution analysis
    sources = {}
    similarity_scores = []
    high_quality_competitors = 0
    
    for result in scored_results:
        source = result.get("source", "unknown")
        sources[source] = sources.get(source, 0) + 1
        similarity_scores.append(result.get("similarity", 0.0))
        
        # High quality = GitHub repos with 100+ stars or high similarity
        if source == "github" and result.get("metadata", {}).get("stars", 0) > 100:
            high_quality_competitors += 1
        elif result.get("similarity", 0) > 0.7:
            high_quality_competitors += 1
    
    # Similarity statistics
    similarity_stats = {
        "avg": statistics.mean(similarity_scores),
        "max": max(similarity_scores),
        "min": min(similarity_scores),
        "std": statistics.stdev(similarity_scores) if len(similarity_scores) > 1 else 0
    }
    
    return {
        "total_competitors": len(scored_results),
        "source_distribution": sources,
        "similarity_stats": {k: round(v, 3) for k, v in similarity_stats.items()},
        "high_quality_competitors": high_quality_competitors,
        "uniqueness_score": uniqueness_score,
        "saturation_level": saturation
    }

def _identify_market_gaps(scored_results: List[Dict], uniqueness_score: float, market_metrics: Dict) -> List[Dict[str, Any]]:
    """Identify specific market gaps from the data"""
    gaps = []
    
    # Gap 1: Blue Ocean Opportunity (high uniqueness + low similarity)
    if uniqueness_score > 0.7 and market_metrics["similarity_stats"]["max"] < 0.6:
        gaps.append({
            "gap_type": "Blue Ocean Opportunity",
            "description": "High uniqueness with low competitor similarity indicates unexplored market space",
            "confidence": 0.9,
            "priority": "Very High",
            "potential_impact": "Market Creation",
            "evidence": f"Uniqueness: {uniqueness_score:.2f}, Max similarity: {market_metrics['similarity_stats']['max']:.2f}"
        })
    
    # Gap 2: Technical Implementation Gap (low GitHub presence)
    github_count = market_metrics["source_distribution"].get("github", 0)
    if github_count < 3:
        gaps.append({
            "gap_type": "Technical Implementation Gap",
            "description": "Limited open-source implementations suggest barriers to entry or untapped technical opportunities",
            "confidence": 0.7,
            "priority": "High",
            "potential_impact": "Technical Differentiation",
            "evidence": f"Only {github_count} GitHub repositories found"
        })
    
    # Gap 3: Feature Gap Analysis (from competitor comments)
    feature_gaps = _extract_feature_gaps(scored_results)
    for gap in feature_gaps:
        gaps.append({
            "gap_type": "Feature Gap",
            "description": f"Missing capability: {gap['feature']}",
            "confidence": gap["confidence"],
            "priority": "Medium",
            "potential_impact": "Product Differentiation",
            "evidence": f"Mentioned in {gap['frequency']} competitor analyses"
        })
    
    # Gap 4: Market Positioning Gap (similarity variance analysis)
    if market_metrics["similarity_stats"]["std"] < 0.15:
        gaps.append({
            "gap_type": "Positioning Opportunity",
            "description": "Low variance in competitor approaches suggests room for differentiated positioning",
            "confidence": 0.6,
            "priority": "Medium",
            "potential_impact": "Market Positioning",
            "evidence": f"Similarity standard deviation: {market_metrics['similarity_stats']['std']:.3f}"
        })
    
    # Gap 5: Quality Gap (few high-quality competitors)
    if market_metrics["high_quality_competitors"] < 2:
        gaps.append({
            "gap_type": "Quality Leadership Opportunity",
            "description": "Few high-quality competitors present opportunity for market leadership",
            "confidence": 0.8,
            "priority": "High", 
            "potential_impact": "Market Leadership",
            "evidence": f"Only {market_metrics['high_quality_competitors']} high-quality competitors identified"
        })
    
    return gaps

def _extract_feature_gaps(scored_results: List[Dict]) -> List[Dict[str, Any]]:
    """Extract commonly mentioned missing features from competitor comments"""
    
    # Keywords that indicate missing features
    gap_indicators = [
        ("lacks", "missing functionality"),
        ("doesn't support", "unsupported features"),
        ("no integration", "integration gaps"),
        ("limited", "capability limitations"),
        ("basic", "feature depth"),
        ("simple", "complexity gaps"),
        ("manual", "automation opportunities")
    ]
    
    feature_mentions = Counter()
    
    for result in scored_results:
        comment = result.get("comment", "").lower()
        for indicator, category in gap_indicators:
            if indicator in comment:
                # Extract surrounding context for the gap
                words = comment.split()
                try:
                    idx = next(i for i, word in enumerate(words) if indicator in word)
                    # Get words around the gap indicator for context
                    context_start = max(0, idx - 2)
                    context_end = min(len(words), idx + 3)
                    context = " ".join(words[context_start:context_end])
                    feature_mentions[category] += 1
                except StopIteration:
                    continue
    
    # Return most commonly mentioned gaps
    gaps = []
    for feature, count in feature_mentions.most_common(3):
        if count > 1:  # Only include gaps mentioned multiple times
            confidence = min(0.9, 0.4 + (count * 0.2))  # Confidence increases with frequency
            gaps.append({
                "feature": feature,
                "frequency": count,
                "confidence": confidence
            })
    
    return gaps

def _calculate_opportunity_score(uniqueness_score: float, market_metrics: Dict, saturation: str) -> Dict[str, Any]:
    """Calculate comprehensive opportunity score"""
    
    # Base score from uniqueness (0-40 points)
    uniqueness_points = uniqueness_score * 40
    
    # Similarity advantage (0-25 points) - lower average similarity is better
    avg_similarity = market_metrics["similarity_stats"]["avg"]
    similarity_points = (1.0 - avg_similarity) * 25
    
    # Competition density (0-20 points) - fewer high-quality competitors is better
    total_competitors = market_metrics["total_competitors"]
    high_quality = market_metrics["high_quality_competitors"]
    
    if total_competitors == 0:
        competition_points = 20
    else:
        competition_density = high_quality / total_competitors
        competition_points = (1.0 - competition_density) * 20
    
    # Market saturation adjustment (0-15 points)
    saturation_points = {
        "Low market saturation": 15,
        "Moderate market saturation": 10,
        "High market saturation": 5,
        "Very high market saturation": 0
    }.get(saturation, 7.5)
    
    # Calculate final score
    raw_score = uniqueness_points + similarity_points + competition_points + saturation_points
    final_score = min(100, max(0, raw_score))
    
    return {
        "overall_score": round(final_score, 1),
        "components": {
            "uniqueness_contribution": round(uniqueness_points, 1),
            "similarity_advantage": round(similarity_points, 1),
            "competition_advantage": round(competition_points, 1),
            "market_saturation_boost": round(saturation_points, 1)
        },
        "interpretation": _interpret_opportunity_score(final_score),
        "confidence_level": _calculate_confidence_level(market_metrics)
    }

def _interpret_opportunity_score(score: float) -> str:
    """Provide human-readable interpretation of opportunity score"""
    if score >= 85:
        return "Exceptional opportunity - dominant market potential with high differentiation"
    elif score >= 70:
        return "Strong opportunity - significant market potential with good differentiation"
    elif score >= 55:
        return "Moderate opportunity - viable market entry with strategic positioning required"
    elif score >= 40:
        return "Limited opportunity - challenging market with established competition"
    else:
        return "Low opportunity - saturated market with strong incumbents"

def _calculate_confidence_level(market_metrics: Dict) -> str:
    """Calculate confidence level in the analysis"""
    total_data_points = market_metrics["total_competitors"]
    source_diversity = len(market_metrics["source_distribution"])
    
    if total_data_points >= 10 and source_diversity >= 3:
        return "High confidence - comprehensive data across multiple sources"
    elif total_data_points >= 5 and source_diversity >= 2:
        return "Medium confidence - adequate data from multiple sources"
    elif total_data_points >= 3:
        return "Low confidence - limited data available for analysis"
    else:
        return "Very low confidence - insufficient data for reliable analysis"

def _determine_market_position(uniqueness_score: float, market_metrics: Dict) -> str:
    """Determine recommended market positioning strategy"""
    avg_similarity = market_metrics["similarity_stats"]["avg"]
    total_competitors = market_metrics["total_competitors"]
    
    if uniqueness_score > 0.8:
        return "Pioneer - create new market category and establish standards"
    elif uniqueness_score > 0.6 and avg_similarity < 0.5:
        return "Differentiator - focus on unique value proposition and innovation"
    elif total_competitors < 5:
        return "Fast follower - improve on existing solutions with better execution"
    elif avg_similarity < 0.4:
        return "Niche specialist - target underserved segments with focused features"
    else:
        return "Cost leader - compete on efficiency, pricing, or specific use cases"

def _analyze_competitive_landscape(scored_results: List[Dict]) -> Dict[str, Any]:
    """Analyze the competitive landscape in detail"""
    
    if not scored_results:
        return {"competitive_threats": [], "market_leaders": [], "weak_competitors": []}
    
    # Categorize competitors by threat level
    competitive_threats = []  # High similarity, strong market presence
    market_leaders = []       # High quality indicators
    weak_competitors = []     # Low quality or similarity
    
    for result in scored_results:
        similarity = result.get("similarity", 0.0)
        metadata = result.get("metadata", {})
        source = result.get("source", "")
        
        # Threat assessment
        threat_level = "Low"
        quality_indicators = []
        
        if similarity > 0.7:
            threat_level = "High"
            quality_indicators.append(f"High similarity ({similarity:.1%})")
        elif similarity > 0.5:
            threat_level = "Medium"
        
        # Additional quality indicators
        if source == "github":
            stars = metadata.get("stars", 0)
            if stars > 1000:
                threat_level = "High" if threat_level != "High" else threat_level
                quality_indicators.append(f"{stars} GitHub stars")
            elif stars > 100:
                quality_indicators.append(f"{stars} GitHub stars")
        
        competitor_info = {
            "name": result.get("title", "Unknown"),
            "source": source,
            "similarity": similarity,
            "threat_level": threat_level,
            "quality_indicators": quality_indicators,
            "url": result.get("url", ""),
            "analysis": result.get("comment", "No analysis available")
        }
        
        # Categorize
        if threat_level == "High":
            competitive_threats.append(competitor_info)
        elif quality_indicators:
            market_leaders.append(competitor_info)
        else:
            weak_competitors.append(competitor_info)
    
    return {
        "competitive_threats": competitive_threats,
        "market_leaders": market_leaders,
        "weak_competitors": weak_competitors,
        "threat_summary": f"{len(competitive_threats)} high-threat competitors identified"
    }

def _generate_strategic_recommendations(analysis: Dict[str, Any]) -> List[Dict[str, str]]:
    """Generate actionable strategic recommendations"""
    recommendations = []
    
    opportunity_score = analysis["opportunity_score"]["overall_score"]
    gaps = analysis["gaps_identified"]
    market_position = analysis["market_position"]
    competitive_threats = len(analysis["competitive_analysis"]["competitive_threats"])
    
    # Strategic timing recommendations
    if opportunity_score > 75:
        recommendations.append({
            "type": "Strategic Timing",
            "priority": "Very High",
            "recommendation": "Move aggressively to capture market opportunity before window closes. Consider rapid MVP development and early customer acquisition."
        })
    elif opportunity_score > 50:
        recommendations.append({
            "type": "Strategic Timing", 
            "priority": "High",
            "recommendation": "Solid market opportunity exists. Develop comprehensive go-to-market strategy with differentiated positioning."
        })
    
    # Gap-specific recommendations
    high_priority_gaps = [gap for gap in gaps if gap.get("priority") in ["Very High", "High"]]
    for gap in high_priority_gaps[:3]:  # Top 3 gaps
        recommendations.append({
            "type": "Product Development",
            "priority": gap["priority"],
            "recommendation": f"Address {gap['gap_type']}: {gap['description']}. Potential impact: {gap.get('potential_impact', 'Unknown')}"
        })
    
    # Competitive strategy
    if competitive_threats > 3:
        recommendations.append({
            "type": "Competitive Strategy",
            "priority": "High",
            "recommendation": "High competitive threat detected. Focus on rapid differentiation and customer lock-in strategies."
        })
    elif competitive_threats == 0:
        recommendations.append({
            "type": "Market Education",
            "priority": "Medium", 
            "recommendation": "No direct competitors found. Budget for market education and category creation efforts."
        })
    
    # Positioning strategy
    recommendations.append({
        "type": "Market Positioning",
        "priority": "Medium",
        "recommendation": f"Adopt '{market_position}' strategy. This aligns with your market opportunity and competitive landscape."
    })
    
    # Resource allocation
    if opportunity_score > 60:
        recommendations.append({
            "type": "Resource Allocation",
            "priority": "Medium",
            "recommendation": "Strong opportunity justifies significant resource investment. Consider seeking funding or partnerships for acceleration."
        })
    
    return recommendations

@app.tool()
def get_server_info() -> Dict[str, Any]:
    return {
        "server_name": "Enhanced Research Gap Detection Server",
        "version": "2.0.0",
        "capabilities": ["analyze_market_gaps"],
        "specialization": "Advanced market gap analysis with competitor intelligence and strategic recommendations",
        "status": "active",
        "input_format": "scored_results with similarity analysis and market data"
    }

if __name__ == "__main__":
    print("🔍 Starting Enhanced Gap Detection MCP Server...")
    print("📡 SSE endpoint at http://localhost:8002/sse")
    print("💡 Enhanced capabilities:")
    print("   • Comprehensive market gap analysis")
    print("   • Competitive landscape assessment")
    print("   • Strategic opportunity scoring")
    print("   • Actionable business recommendations")
    print("   • Multi-source data integration")
    
    sse_app = create_sse_app(app, message_path="/", sse_path="/sse")
    uvicorn.run(sse_app, host="0.0.0.0", port=8002, log_level="info")