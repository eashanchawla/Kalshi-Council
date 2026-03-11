"""Market Analyzer and Web Researcher modules using Claude for analysis and evidence gathering."""

import anthropic

DEFAULT_MODEL = "claude-sonnet-4-20250514"


class MarketAnalyzer:
    """Parses market questions, identifies key claims, and extracts research topics."""

    def __init__(self, client: anthropic.Anthropic | None = None, model: str = DEFAULT_MODEL):
        self.client = client or anthropic.Anthropic()
        self.model = model

    def analyze(self, market_metadata: dict) -> dict:
        """Analyze a market question to extract claims and research topics.

        Returns a dict with keys: key_claims, research_topics, context_summary.
        """
        title = market_metadata.get("title", "")
        subtitle = market_metadata.get("subtitle", "")
        close_time = market_metadata.get("close_time", "")

        prompt = f"""Analyze this prediction market question and provide a structured breakdown.

Market Question: {title}
Additional Context: {subtitle}
Market Closes: {close_time}

Respond in this exact format:

KEY CLAIMS:
- [List each testable claim or condition in the market question]

RESEARCH TOPICS:
- [List specific topics to research to evaluate this market]

CONTEXT SUMMARY:
[One paragraph summarizing what this market is about and what would need to happen for YES/NO outcomes]"""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}],
        )

        text = response.content[0].text
        return self._parse_analysis(text)

    def _parse_analysis(self, text: str) -> dict:
        """Parse the structured analysis response into a dict."""
        result = {"key_claims": [], "research_topics": [], "context_summary": ""}

        current_section = None
        for line in text.split("\n"):
            line = line.strip()
            if "KEY CLAIMS" in line.upper():
                current_section = "key_claims"
            elif "RESEARCH TOPICS" in line.upper():
                current_section = "research_topics"
            elif "CONTEXT SUMMARY" in line.upper():
                current_section = "context_summary"
            elif line.startswith("- ") and current_section in ("key_claims", "research_topics"):
                result[current_section].append(line[2:])
            elif current_section == "context_summary" and line:
                if result["context_summary"]:
                    result["context_summary"] += " " + line
                else:
                    result["context_summary"] = line

        return result


class WebResearcher:
    """Uses Claude with web search to gather evidence for market analysis."""

    def __init__(self, client: anthropic.Anthropic | None = None, model: str = DEFAULT_MODEL):
        self.client = client or anthropic.Anthropic()
        self.model = model

    def research(self, market_metadata: dict, analysis: dict) -> dict:
        """Conduct web research on a market question.

        Returns a dict with keys: evidence_summary, sources, key_findings.
        """
        title = market_metadata.get("title", "")
        topics = analysis.get("research_topics", [])
        claims = analysis.get("key_claims", [])

        topics_str = "\n".join(f"- {t}" for t in topics)
        claims_str = "\n".join(f"- {c}" for c in claims)

        prompt = f"""Research this prediction market question using web search. Find the most current and relevant information.

Market Question: {title}

Key Claims to Investigate:
{claims_str}

Research Topics:
{topics_str}

Search for the latest news, data, and expert opinions. Then provide your findings in this exact format:

KEY FINDINGS:
- [List each important finding with its source]

EVIDENCE SUMMARY:
[Comprehensive paragraph summarizing all evidence found, distinguishing facts from speculation]

SOURCES:
- [List each source URL or reference used]"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}],
                tools=[{"type": "web_search_20250305"}],
            )

            text = self._extract_text(response)
        except anthropic.APIError:
            # Fall back to non-web-search if web search isn't available
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}],
            )
            text = response.content[0].text

        return self._parse_research(text)

    def _extract_text(self, response) -> str:
        """Extract text content from a response that may include tool use blocks."""
        parts = []
        for block in response.content:
            if hasattr(block, "text"):
                parts.append(block.text)
        return "\n".join(parts)

    def _parse_research(self, text: str) -> dict:
        """Parse research response into structured dict."""
        result = {"key_findings": [], "evidence_summary": "", "sources": []}

        current_section = None
        for line in text.split("\n"):
            line = line.strip()
            if "KEY FINDINGS" in line.upper():
                current_section = "key_findings"
            elif "EVIDENCE SUMMARY" in line.upper():
                current_section = "evidence_summary"
            elif "SOURCES" in line.upper() and "EVIDENCE" not in line.upper():
                current_section = "sources"
            elif line.startswith("- ") and current_section in ("key_findings", "sources"):
                result[current_section].append(line[2:])
            elif current_section == "evidence_summary" and line:
                if result["evidence_summary"]:
                    result["evidence_summary"] += " " + line
                else:
                    result["evidence_summary"] = line

        return result
