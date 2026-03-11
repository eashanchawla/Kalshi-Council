"""Consensus Engine - aggregates council member analyses into a unified prediction."""

import anthropic

DEFAULT_MODEL = "claude-sonnet-4-20250514"


class ConsensusEngine:
    """Synthesizes individual council analyses into a consensus prediction."""

    def __init__(self, client: anthropic.Anthropic | None = None, model: str = DEFAULT_MODEL):
        self.client = client or anthropic.Anthropic()
        self.model = model

    def generate_consensus(self, market_metadata: dict, analyses: list[dict]) -> dict:
        """Generate a consensus from multiple council member analyses.

        Args:
            market_metadata: Market information dict.
            analyses: List of analysis dicts from each council member.

        Returns:
            Dict with: consensus_probability, confidence, agreements, disagreements, synthesis.
        """
        # Calculate weighted average probability
        weights = {"high": 1.2, "medium": 1.0, "low": 0.8}
        total_weight = 0.0
        weighted_sum = 0.0
        for a in analyses:
            w = weights.get(a.get("confidence", "medium"), 1.0)
            weighted_sum += a["probability"] * w
            total_weight += w

        avg_probability = round(weighted_sum / total_weight) if total_weight else 50

        # Use Claude to synthesize qualitative consensus
        analyses_text = self._format_analyses(analyses)
        title = market_metadata.get("title", "")

        prompt = f"""You are the moderator of a prediction market investment council.
Synthesize these independent analyses into a consensus view.

Market Question: {title}

{analyses_text}

Weighted Average Probability: {avg_probability}%

Provide your synthesis in this exact format:

AREAS OF AGREEMENT:
- [Points where analysts broadly agree]

KEY DISAGREEMENTS:
- [Points where analysts disagree, and why]

CONFIDENCE ASSESSMENT:
[Overall confidence score 0-100 and brief justification]

FINAL CONSENSUS:
[1-2 sentence summary of the council's collective view]"""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}],
        )

        text = response.content[0].text
        parsed = self._parse_synthesis(text)

        # Adjust confidence based on analyst agreement spread
        spread = max(a["probability"] for a in analyses) - min(a["probability"] for a in analyses)
        spread_penalty = min(spread / 2, 20)  # Large spread reduces confidence
        adjusted_confidence = max(0, min(100, parsed["confidence"] - int(spread_penalty)))

        return {
            "consensus_probability": avg_probability,
            "confidence": adjusted_confidence,
            "agreements": parsed["agreements"],
            "disagreements": parsed["disagreements"],
            "synthesis": parsed["synthesis"],
            "individual_analyses": analyses,
            "probability_spread": spread,
        }

    def _format_analyses(self, analyses: list[dict]) -> str:
        """Format analyses for the synthesis prompt."""
        parts = []
        for a in analyses:
            factors_for = "\n  ".join(f"+ {f}" for f in a.get("factors_for", []))
            factors_against = "\n  ".join(f"- {f}" for f in a.get("factors_against", []))
            parts.append(
                f"--- {a['name']} ({a['role']}) ---\n"
                f"Probability: {a['probability']}%\n"
                f"Confidence: {a['confidence']}\n"
                f"Reasoning: {a['reasoning']}\n"
                f"Supporting Factors:\n  {factors_for}\n"
                f"Opposing Factors:\n  {factors_against}"
            )
        return "\n\n".join(parts)

    def _parse_synthesis(self, text: str) -> dict:
        """Parse the synthesis response."""
        result = {"agreements": [], "disagreements": [], "confidence": 50, "synthesis": ""}

        current_section = None
        for line in text.split("\n"):
            line = line.strip()
            upper = line.upper()
            if "AREAS OF AGREEMENT" in upper:
                current_section = "agreements"
            elif "KEY DISAGREEMENT" in upper:
                current_section = "disagreements"
            elif "CONFIDENCE ASSESSMENT" in upper:
                current_section = "confidence_text"
            elif "FINAL CONSENSUS" in upper:
                current_section = "synthesis"
            elif line.startswith("- ") and current_section in ("agreements", "disagreements"):
                result[current_section].append(line[2:])
            elif current_section == "confidence_text" and line:
                # Try to extract a number from the confidence line
                for word in line.split():
                    try:
                        num = int(word.strip(":/,;."))
                        if 0 <= num <= 100:
                            result["confidence"] = num
                            break
                    except ValueError:
                        continue
            elif current_section == "synthesis" and line:
                if result["synthesis"]:
                    result["synthesis"] += " " + line
                else:
                    result["synthesis"] = line

        return result
