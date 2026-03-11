"""LLM Council Members - three specialized analyst personas for independent market analysis."""

import json
import re

import anthropic

DEFAULT_MODEL = "claude-sonnet-4-20250514"

COUNCIL_MEMBERS = [
    {
        "name": "Alex the Analyst",
        "role": "Quantitative Analyst",
        "system_prompt": (
            "You are Alex, a quantitative analyst on a prediction market investment council. "
            "Your expertise is in statistical reasoning, mathematical edges, and base rate analysis. "
            "You focus on data-driven insights, are skeptical of narratives, and look for testable "
            "hypotheses. Your guiding question is: 'What do the numbers actually tell us?' "
            "You identify when markets are mispriced mathematically and look for statistical edges."
        ),
    },
    {
        "name": "Jordan the Journalist",
        "role": "Research Analyst",
        "system_prompt": (
            "You are Jordan, an investigative journalist on a prediction market investment council. "
            "Your expertise is in evidence quality, news research, and source validation. "
            "You find the latest information and separate signal from noise. You maintain rigorous "
            "evidence standards, fact-check claims, and identify misinformation. "
            "Your guiding question is: 'What's the strongest recent evidence?'"
        ),
    },
    {
        "name": "Casey the Contrarian",
        "role": "Risk Analyst",
        "system_prompt": (
            "You are Casey, a contrarian risk analyst on a prediction market investment council. "
            "Your expertise is in challenging consensus, identifying blind spots, and spotting risks "
            "others miss. You play devil's advocate, explore failure modes, and highlight "
            "uncertainties. Your guiding question is: 'What could everyone be wrong about?' "
            "You question assumptions and look for scenarios where conventional wisdom fails."
        ),
    },
]


class CouncilMember:
    """A single council member that independently analyzes a prediction market."""

    def __init__(
        self,
        name: str,
        role: str,
        system_prompt: str,
        client: anthropic.Anthropic | None = None,
        model: str = DEFAULT_MODEL,
    ):
        self.name = name
        self.role = role
        self.system_prompt = system_prompt
        self.client = client or anthropic.Anthropic()
        self.model = model

    def analyze(self, market_metadata: dict, research: dict) -> dict:
        """Produce an independent analysis of the market.

        Returns dict with: probability, confidence, factors, reasoning.
        """
        title = market_metadata.get("title", "")
        yes_price = market_metadata.get("yes_price", 0)
        evidence = research.get("evidence_summary", "No research available.")
        findings = research.get("key_findings", [])
        findings_str = "\n".join(f"- {f}" for f in findings) if findings else "None available."

        prompt = f"""Analyze this prediction market and provide your independent assessment.

Market Question: {title}
Current Market Price (YES): {yes_price}¢

Research Findings:
{findings_str}

Evidence Summary:
{evidence}

Provide your analysis in this exact JSON format (no other text):
{{
    "probability": <your estimated probability 0-100>,
    "confidence": "<low|medium|high>",
    "factors_for": ["<factor supporting YES>", ...],
    "factors_against": ["<factor supporting NO>", ...],
    "reasoning": "<2-3 sentence summary of your analysis>"
}}"""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            system=self.system_prompt,
            messages=[{"role": "user", "content": prompt}],
        )

        text = response.content[0].text
        return self._parse_response(text)

    def _parse_response(self, text: str) -> dict:
        """Parse the JSON response from the council member."""
        # Try to extract JSON from the response
        json_match = re.search(r"\{[\s\S]*\}", text)
        if json_match:
            try:
                parsed = json.loads(json_match.group())
                return {
                    "name": self.name,
                    "role": self.role,
                    "probability": int(parsed.get("probability", 50)),
                    "confidence": parsed.get("confidence", "medium"),
                    "factors_for": parsed.get("factors_for", []),
                    "factors_against": parsed.get("factors_against", []),
                    "reasoning": parsed.get("reasoning", ""),
                }
            except (json.JSONDecodeError, ValueError):
                pass

        # Fallback if parsing fails
        return {
            "name": self.name,
            "role": self.role,
            "probability": 50,
            "confidence": "low",
            "factors_for": [],
            "factors_against": [],
            "reasoning": f"Failed to parse structured response. Raw: {text[:200]}",
        }


def create_council(client: anthropic.Anthropic | None = None, model: str = DEFAULT_MODEL) -> list[CouncilMember]:
    """Create the default council of three members."""
    return [
        CouncilMember(
            name=m["name"],
            role=m["role"],
            system_prompt=m["system_prompt"],
            client=client,
            model=model,
        )
        for m in COUNCIL_MEMBERS
    ]
