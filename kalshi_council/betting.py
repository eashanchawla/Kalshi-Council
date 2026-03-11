"""Betting Decision Module - calculates edge, expected value, and generates recommendations."""

from dataclasses import dataclass
from enum import Enum


class Recommendation(Enum):
    BUY_YES = "BUY_YES"
    BUY_NO = "BUY_NO"
    PASS = "PASS"


@dataclass
class BettingDecision:
    recommendation: Recommendation
    edge: float
    expected_value: float
    bet_size: float
    confidence: int
    consensus_probability: int
    market_price_yes: int
    reasoning: str

    def to_dict(self) -> dict:
        return {
            "recommendation": self.recommendation.value,
            "edge": round(self.edge, 2),
            "expected_value": round(self.expected_value, 2),
            "bet_size": self.bet_size,
            "confidence": self.confidence,
            "consensus_probability": self.consensus_probability,
            "market_price_yes": self.market_price_yes,
            "reasoning": self.reasoning,
        }


class BettingDecisionModule:
    """Calculates expected value and generates betting recommendations."""

    def __init__(
        self,
        min_edge: float = 5.0,
        min_confidence: int = 40,
        default_bet_size: float = 5.0,
    ):
        self.min_edge = min_edge
        self.min_confidence = min_confidence
        self.default_bet_size = default_bet_size

    def decide(self, consensus: dict, market_metadata: dict) -> BettingDecision:
        """Generate a betting decision from consensus and market data.

        Args:
            consensus: Dict from ConsensusEngine with consensus_probability and confidence.
            market_metadata: Dict with yes_price (in cents, 0-100).

        Returns:
            BettingDecision with recommendation, edge, EV, and reasoning.
        """
        council_prob = consensus["consensus_probability"]
        confidence = consensus["confidence"]
        market_yes = market_metadata.get("yes_price", 50)

        # Edge on YES side: council thinks YES is more likely than market implies
        edge_yes = council_prob - market_yes
        # Edge on NO side: council thinks NO is more likely than market implies
        edge_no = (100 - council_prob) - (100 - market_yes)  # equivalent to market_yes - council_prob

        # Determine which side has the edge
        if abs(edge_yes) >= abs(edge_no):
            edge = edge_yes
            side = "YES"
        else:
            edge = -edge_no  # make it positive if NO has edge
            side = "NO"

        # Calculate expected value per dollar
        if side == "YES":
            # Buying YES at market_yes cents, pays 100 cents if correct
            cost = market_yes / 100
            win_prob = council_prob / 100
            ev = (win_prob * (1 - cost)) - ((1 - win_prob) * cost)
        else:
            # Buying NO at (100 - market_yes) cents, pays 100 cents if correct
            cost = (100 - market_yes) / 100
            win_prob = (100 - council_prob) / 100
            ev = (win_prob * (1 - cost)) - ((1 - win_prob) * cost)

        ev_per_dollar = ev  # net return per dollar risked

        # Decision logic
        abs_edge = abs(edge_yes) if side == "YES" else abs(edge_no)

        if confidence < self.min_confidence:
            recommendation = Recommendation.PASS
            reasoning = f"Confidence too low: {confidence} < {self.min_confidence}"
        elif abs_edge < self.min_edge:
            recommendation = Recommendation.PASS
            reasoning = f"Insufficient edge: {abs_edge:.1f}% < {self.min_edge}%"
        elif side == "YES" and edge_yes > 0:
            recommendation = Recommendation.BUY_YES
            reasoning = (
                f"Council probability ({council_prob}%) exceeds market ({market_yes}¢) "
                f"by {edge_yes:.1f}%. EV: {ev_per_dollar:+.3f} per dollar."
            )
        elif side == "NO" and edge_no < 0:
            recommendation = Recommendation.BUY_NO
            reasoning = (
                f"Council probability ({council_prob}%) below market ({market_yes}¢) "
                f"by {abs(edge_no):.1f}%. NO side EV: {ev_per_dollar:+.3f} per dollar."
            )
        else:
            recommendation = Recommendation.PASS
            reasoning = f"No clear edge identified. Edge YES: {edge_yes:.1f}%, Edge NO: {edge_no:.1f}%"

        return BettingDecision(
            recommendation=recommendation,
            edge=abs_edge,
            expected_value=round(ev_per_dollar * self.default_bet_size, 2),
            bet_size=self.default_bet_size,
            confidence=confidence,
            consensus_probability=council_prob,
            market_price_yes=market_yes,
            reasoning=reasoning,
        )
