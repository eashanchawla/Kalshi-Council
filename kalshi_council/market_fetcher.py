"""Market Fetcher module for retrieving prediction markets from Kalshi's public API."""

import random
from typing import Optional

import requests

KALSHI_BASE_URL = "https://api.elections.kalshi.com/trade-api/v2"

CATEGORY_KEYWORDS = {
    "politics": ["election", "president", "congress", "senate", "governor", "trump", "biden", "political", "vote"],
    "economics": ["inflation", "fed", "interest rate", "gdp", "unemployment", "recession", "stock", "s&p", "nasdaq"],
    "sports": ["nfl", "nba", "mlb", "nhl", "super bowl", "world series", "championship", "game", "match"],
    "tech": ["ai", "apple", "google", "microsoft", "tesla", "openai", "launch", "ipo", "tech"],
    "climate": ["temperature", "hurricane", "weather", "climate", "wildfire", "earthquake", "storm"],
    "entertainment": ["oscar", "grammy", "emmy", "box office", "movie", "album", "tv", "streaming"],
}


class MarketFetcher:
    """Fetches and filters prediction markets from the Kalshi public API."""

    def __init__(self, base_url: str = KALSHI_BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})

    def fetch_markets(self, limit: int = 200, status: str = "open") -> list[dict]:
        """Fetch open markets from Kalshi."""
        url = f"{self.base_url}/markets"
        params = {"status": status, "limit": limit}

        response = self.session.get(url, params=params, timeout=30)
        response.raise_for_status()

        data = response.json()
        return data.get("markets", [])

    def filter_by_category(self, markets: list[dict], category: str) -> list[dict]:
        """Filter markets by category using keyword matching."""
        category = category.lower()
        keywords = CATEGORY_KEYWORDS.get(category, [])

        if not keywords:
            raise ValueError(f"Unknown category: {category}. Valid: {list(CATEGORY_KEYWORDS.keys())}")

        filtered = []
        for market in markets:
            title = (market.get("title") or "").lower()
            subtitle = (market.get("subtitle") or "").lower()
            text = f"{title} {subtitle}"
            if any(kw in text for kw in keywords):
                filtered.append(market)
        return filtered

    def get_random_market(self, category: Optional[str] = None) -> dict:
        """Fetch a random open market, optionally filtered by category."""
        markets = self.fetch_markets()

        if not markets:
            raise RuntimeError("No open markets found on Kalshi.")

        if category:
            markets = self.filter_by_category(markets, category)
            if not markets:
                raise RuntimeError(f"No open markets found in category: {category}")

        return random.choice(markets)

    def get_orderbook(self, ticker: str) -> dict:
        """Fetch orderbook data for a specific market ticker."""
        url = f"{self.base_url}/markets/{ticker}/orderbook"
        response = self.session.get(url, timeout=30)
        response.raise_for_status()
        return response.json().get("orderbook", {})

    def get_market_details(self, ticker: str) -> dict:
        """Fetch detailed information for a specific market."""
        url = f"{self.base_url}/markets/{ticker}"
        response = self.session.get(url, timeout=30)
        response.raise_for_status()
        return response.json().get("market", {})

    def extract_market_metadata(self, market: dict) -> dict:
        """Extract key metadata from a market dict into a clean structure."""
        yes_price = market.get("yes_bid") or market.get("last_price") or 0
        no_price = market.get("no_bid") or (100 - yes_price) if yes_price else 0

        return {
            "ticker": market.get("ticker", ""),
            "title": market.get("title", ""),
            "subtitle": market.get("subtitle", ""),
            "category": market.get("category", ""),
            "status": market.get("status", ""),
            "yes_price": yes_price,
            "no_price": no_price,
            "volume": market.get("volume", 0),
            "open_interest": market.get("open_interest", 0),
            "close_time": market.get("close_time", ""),
        }
