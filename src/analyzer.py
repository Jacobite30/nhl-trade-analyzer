"""AI-powered trade analysis engine using OpenAI."""

import json
from openai import OpenAI


SYSTEM_PROMPT = """You are an expert NHL trade analyst with deep knowledge of:
- Player valuations and contract analysis
- Salary cap implications and management
- Team building strategies and roster construction
- Draft pick value charts and prospect evaluation
- Historical trade comparisons
- Advanced hockey analytics (xG, WAR, GAR, RAPM)

When analyzing a trade, provide a comprehensive, balanced analysis. Be specific with your reasoning
and reference real NHL context where relevant. Format your response as a structured JSON object."""


def build_trade_prompt(team1_name, team1_assets, team2_name, team2_assets):
    """Build the trade analysis prompt."""
    team1_items = []
    for asset in team1_assets:
        if asset["type"] == "player":
            detail = f"Player: {asset['name']}"
            if asset.get("position"):
                detail += f" ({asset['position']})"
            if asset.get("cap_hit"):
                detail += f" - Cap Hit: ${asset['cap_hit']}"
            if asset.get("contract_years"):
                detail += f" - {asset['contract_years']} years remaining"
            if asset.get("age"):
                detail += f" - Age: {asset['age']}"
            if asset.get("retention"):
                detail += f" - Salary Retention: {asset['retention']}"
            team1_items.append(detail)
        elif asset["type"] == "pick":
            team1_items.append(f"Draft Pick: {asset['name']}")
        elif asset["type"] == "prospect":
            detail = f"Prospect: {asset['name']}"
            if asset.get("position"):
                detail += f" ({asset['position']})"
            team1_items.append(detail)

    team2_items = []
    for asset in team2_assets:
        if asset["type"] == "player":
            detail = f"Player: {asset['name']}"
            if asset.get("position"):
                detail += f" ({asset['position']})"
            if asset.get("cap_hit"):
                detail += f" - Cap Hit: ${asset['cap_hit']}"
            if asset.get("contract_years"):
                detail += f" - {asset['contract_years']} years remaining"
            if asset.get("age"):
                detail += f" - Age: {asset['age']}"
            if asset.get("retention"):
                detail += f" - Salary Retention: {asset['retention']}"
            team2_items.append(detail)
        elif asset["type"] == "pick":
            team2_items.append(f"Draft Pick: {asset['name']}")
        elif asset["type"] == "prospect":
            detail = f"Prospect: {asset['name']}"
            if asset.get("position"):
                detail += f" ({asset['position']})"
            team2_items.append(detail)

    prompt = f"""Analyze the following NHL trade:

**{team1_name} sends:**
{chr(10).join('- ' + item for item in team1_items)}

**{team2_name} sends:**
{chr(10).join('- ' + item for item in team2_items)}

Provide your analysis as a JSON object with EXACTLY this structure:
{{
    "trade_grade_team1": "A letter grade from A+ to F for {team1_name}",
    "trade_grade_team2": "A letter grade from A+ to F for {team2_name}",
    "winner": "The team name that wins this trade, or 'Even' if fair",
    "summary": "A 2-3 sentence overall summary of the trade",
    "team1_analysis": {{
        "pros": ["list of 2-4 pros for {team1_name}"],
        "cons": ["list of 2-4 cons for {team1_name}"],
        "cap_impact": "Brief cap impact analysis for {team1_name}",
        "window_impact": "How this affects {team1_name}'s competitive window"
    }},
    "team2_analysis": {{
        "pros": ["list of 2-4 pros for {team2_name}"],
        "cons": ["list of 2-4 cons for {team2_name}"],
        "cap_impact": "Brief cap impact analysis for {team2_name}",
        "window_impact": "How this affects {team2_name}'s competitive window"
    }},
    "historical_comparison": "Compare this trade to a similar historical NHL trade",
    "fairness_score": "A number from 1-10 where 5 is perfectly fair, <5 favors {team1_name}, >5 favors {team2_name}"
}}

Return ONLY the JSON object, no other text."""

    return prompt


def analyze_trade(api_key, team1_name, team1_assets, team2_name, team2_assets, model="gpt-4o"):
    """
    Analyze a trade using OpenAI API.

    Returns a dict with the analysis results or an error message.
    """
    if not api_key:
        return {"error": "Please enter your OpenAI API key in Settings."}

    if not team1_assets:
        return {"error": f"Please add at least one asset for {team1_name}."}

    if not team2_assets:
        return {"error": f"Please add at least one asset for {team2_name}."}

    try:
        client = OpenAI(api_key=api_key)
        prompt = build_trade_prompt(team1_name, team1_assets, team2_name, team2_assets)

        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=2000,
        )

        content = response.choices[0].message.content.strip()

        # Try to extract JSON from the response
        if content.startswith("```"):
            # Remove markdown code block
            lines = content.split("\n")
            content = "\n".join(lines[1:-1])

        result = json.loads(content)
        return result

    except json.JSONDecodeError:
        return {"error": "Failed to parse AI response. Please try again."}
    except Exception as e:
        error_msg = str(e)
        if "api_key" in error_msg.lower() or "auth" in error_msg.lower():
            return {"error": "Invalid API key. Please check your OpenAI API key in Settings."}
        if "model" in error_msg.lower():
            return {"error": f"Model '{model}' is not available. Try using 'gpt-4o-mini' or 'gpt-3.5-turbo'."}
        return {"error": f"Analysis failed: {error_msg}"}


def format_analysis_text(result, team1_name, team2_name):
    """Format the analysis result into readable text."""
    if "error" in result:
        return f"Error: {result['error']}"

    lines = []
    lines.append("=" * 60)
    lines.append("         NHL TRADE ANALYSIS REPORT")
    lines.append("=" * 60)
    lines.append("")

    # Summary
    lines.append(f"SUMMARY: {result.get('summary', 'N/A')}")
    lines.append("")

    # Trade Grades
    grade1 = result.get("trade_grade_team1", "N/A")
    grade2 = result.get("trade_grade_team2", "N/A")
    winner = result.get("winner", "N/A")
    fairness = result.get("fairness_score", "N/A")

    lines.append("-" * 40)
    lines.append("TRADE GRADES")
    lines.append("-" * 40)
    lines.append(f"  {team1_name}: {grade1}")
    lines.append(f"  {team2_name}: {grade2}")
    lines.append(f"  Winner: {winner}")
    lines.append(f"  Fairness Score: {fairness}/10")
    lines.append("")

    # Team 1 Analysis
    t1 = result.get("team1_analysis", {})
    lines.append("-" * 40)
    lines.append(f"{team1_name.upper()} ANALYSIS")
    lines.append("-" * 40)

    lines.append("  Pros:")
    for pro in t1.get("pros", []):
        lines.append(f"    + {pro}")

    lines.append("  Cons:")
    for con in t1.get("cons", []):
        lines.append(f"    - {con}")

    lines.append(f"  Cap Impact: {t1.get('cap_impact', 'N/A')}")
    lines.append(f"  Window Impact: {t1.get('window_impact', 'N/A')}")
    lines.append("")

    # Team 2 Analysis
    t2 = result.get("team2_analysis", {})
    lines.append("-" * 40)
    lines.append(f"{team2_name.upper()} ANALYSIS")
    lines.append("-" * 40)

    lines.append("  Pros:")
    for pro in t2.get("pros", []):
        lines.append(f"    + {pro}")

    lines.append("  Cons:")
    for con in t2.get("cons", []):
        lines.append(f"    - {con}")

    lines.append(f"  Cap Impact: {t2.get('cap_impact', 'N/A')}")
    lines.append(f"  Window Impact: {t2.get('window_impact', 'N/A')}")
    lines.append("")

    # Historical Comparison
    lines.append("-" * 40)
    lines.append("HISTORICAL COMPARISON")
    lines.append("-" * 40)
    lines.append(f"  {result.get('historical_comparison', 'N/A')}")
    lines.append("")
    lines.append("=" * 60)

    return "\n".join(lines)
