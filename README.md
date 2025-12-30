# Kalshi LLM Council Betting System

A sophisticated autonomous betting system that uses multiple LLM models working together as a council to research, analyze, and make consensus predictions on Kalshi prediction markets.

## 🎯 Overview

This project implements a **multi-model LLM consensus framework** that:

1. **Autonomously selects** random prediction market questions from Kalshi
2. **Conducts research** using web search and Claude's reasoning capabilities
3. **Generates independent analyses** from three specialized LLM perspectives
4. **Synthesizes consensus** by weighing multiple viewpoints and identifying areas of agreement/disagreement
5. **Executes betting decisions** based on expected value calculations and confidence levels

The system operates as an **investment council** where each member brings different analytical expertise, creating a more robust prediction through collaborative intelligence rather than relying on a single model's judgment.

## 🏗️ Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────────┐
│                     KALSHI PREDICTION MARKETS                   │
│              (Public API for market data - no auth required)     │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
        ┌────────────────────────────────────┐
        │   Market Fetcher                   │
        │  • Get random/filtered markets     │
        │  • Fetch orderbook data            │
        │  • Extract market metadata         │
        └────────────┬───────────────────────┘
                     │
                     ▼
        ┌────────────────────────────────────┐
        │   Market Analyzer                  │
        │  • Parse market question           │
        │  • Identify key claims             │
        │  • Extract research topics         │
        └────────────┬───────────────────────┘
                     │
                     ▼
        ┌────────────────────────────────────┐
        │   Web Researcher (Claude + Search) │
        │  • Search for current information  │
        │  • Fetch relevant articles         │
        │  • Compile evidence summary        │
        └────────────┬───────────────────────┘
                     │
         ┌───────────┴──────────────┐
         │                          │
         ▼                          ▼
    ┌──────────┐            ┌──────────┐
    │ Research │            │ Research │
    │  Summary │            │  Summary │
    └────┬─────┘            └────┬─────┘
         │                       │
         ▼                       ▼
    ┌─────────────────────────────────────────────────────────────┐
    │                    LLM COUNCIL ANALYSIS                      │
    │  ┌──────────────────┬──────────────────┬──────────────────┐ │
    │  │   Alex Analyst   │  Jordan Reporter │  Casey Contrarian│ │
    │  │                  │                  │                  │ │
    │  │ • Quantitative   │ • Evidence-based │ • Devil's Advocate│ │
    │  │   focus          │   journalism     │ • Risk identifier│ │
    │  │ • Statistical    │ • News research  │ • Blind spot     │ │
    │  │   edges          │ • Source quality │   detection      │ │
    │  │                  │   validation     │                  │ │
    │  └────────┬─────────┴────────┬─────────┴────────┬─────────┘ │
    │           │ Probability      │ Probability      │ Probability│
    │           │ + Factors        │ + Factors        │ + Factors  │
    └───────────┼──────────────────┼──────────────────┼────────────┘
                │                  │                  │
                └──────────────────┬──────────────────┘
                                   │
                                   ▼
            ┌──────────────────────────────────────┐
            │     Consensus Engine                 │
            │  • Aggregate probabilities           │
            │  • Calculate weighted average        │
            │  • Identify agreement zones          │
            │  • Flag disagreements & uncertainties│
            │  • Assess overall confidence         │
            └────────────┬─────────────────────────┘
                         │
                         ▼
            ┌──────────────────────────────────────┐
            │  Betting Decision Module             │
            │  • Compare council vs market price   │
            │  • Calculate edge & expected value   │
            │  • Determine bet size (Kelly/fixed)  │
            │  • Generate recommendation           │
            │    (BUY_YES / BUY_NO / PASS)        │
            └────────────┬─────────────────────────┘
                         │
                         ▼
            ┌──────────────────────────────────────┐
            │     Execution Engine                 │
            │  ┌──────────────────────────────────┐│
            │  │  Dry Run (Testing/Simulation)    ││
            │  │  • No real capital deployed      ││
            │  │  • Full decision logging         ││
            │  │  • Performance tracking          ││
            │  └──────────────────────────────────┘│
            │  ┌──────────────────────────────────┐│
            │  │  Live Trading (Authenticated API)││
            │  │  • Place real orders             ││
            │  │  • RSA signature authentication  ││
            │  │  • Order status monitoring       ││
            │  │  • Portfolio tracking            ││
            │  └──────────────────────────────────┘│
            └──────────────────────────────────────┘
```

### Data Flow

```
Market Selection
      ↓
Research & Evidence Gathering
      ↓
Parallel Independent Analysis (3 models)
      ↓
Consensus & Disagreement Analysis
      ↓
Expected Value Calculation
      ↓
Betting Decision (with confidence scoring)
      ↓
Execution (Dry Run or Live)
      ↓
Logging & Performance Tracking
```

## 📦 Project Structure

```
kalshi-llm-council/
├── kalshi_council_bot.py           # Main executable - complete implementation
├── kalshi_llm_council_guide.md     # Detailed technical documentation
└── README.md                        # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Anthropic API key (for Claude access)
- Kalshi account (optional - required for live trading only)

### Installation

```bash
# Clone or download the project
cd kalshi-llm-council

# Install dependencies
pip install anthropic requests cryptography

# Set environment variables
export ANTHROPIC_API_KEY="your-api-key-here"
export KALSHI_API_KEY_ID="your-kalshi-key-id"        # For live trading
export KALSHI_PRIVATE_KEY="your-kalshi-private-key"  # For live trading
```

### Run a Council Session

```bash
# Run with random market (any category)
python kalshi_council_bot.py

# Run with specific category (politics, economics, sports, tech, climate, entertainment)
python kalshi_council_bot.py politics
python kalshi_council_bot.py economics
python kalshi_council_bot.py sports
```

### Example Output

```
======================================================================
KALSHI PREDICTION MARKET - LLM COUNCIL BETTING SYSTEM
======================================================================

[1/5] Fetching random market...
✓ Found: Will Trump be convicted in federal criminal court by end of 2025?

[2/5] Researching market...
✓ Research complete

[3/5] Council analyzing...
  → Alex the Analyst analyzing...
  → Jordan the Journalist analyzing...
  → Casey the Contrarian analyzing...
✓ All analysts have submitted their analyses

[4/5] Generating consensus...
✓ Consensus generated

[5/5] Processing betting decision...
✓ Decision processed

======================================================================
COUNCIL DECISION SUMMARY
======================================================================

Market: Will Trump be convicted in federal criminal court by end of 2025?
Category: politics
Current Market Price (YES): 28¢

--- Individual Analyses ---
✓ Alex the Analyst: 35% (high)
→ Jordan the Journalist: 32% (medium)
⚠️ Casey the Contrarian: 28% (low)

--- Consensus ---
Consensus Probability: 32%
Recommendation: PASS
Confidence: 67/100

--- Areas of Agreement ---
  • Legal proceedings have significant uncertainty
  • Timeline is constrained (before end of 2025)
  • Multiple legal cases with different probabilities

--- Key Disagreements ---
  • Alex sees higher conviction probability due to pending cases
  • Casey emphasizes legal system delays and barriers

--- Execution ---
Status: PASSED
Reason: Insufficient edge: 4.0%

✓ Results saved to JSON file
```

## 🧠 Council Member Roles

The system uses three specialized LLM personas, each bringing different analytical strengths:

### 1. **Alex the Analyst** (Quantitative Focus)
- **Expertise**: Statistical reasoning, mathematical edges, base rate analysis
- **Strength**: Identifies when markets are mispriced mathematically
- **Approach**: Data-driven, skeptical of narratives, looks for testable hypotheses
- **Question**: "What do the numbers actually tell us?"

### 2. **Jordan the Journalist** (Research Quality)
- **Expertise**: Evidence quality, news research, source validation
- **Strength**: Finds latest information and separates signal from noise
- **Approach**: Rigorous evidence standards, fact-checking, identifying misinformation
- **Question**: "What's the strongest recent evidence?"

### 3. **Casey the Contrarian** (Risk Identification)
- **Expertise**: Challenging consensus, identifying blind spots
- **Strength**: Spots risks others miss, questions assumptions
- **Approach**: Devil's advocate, explores failure modes, highlights uncertainties
- **Question**: "What could everyone be wrong about?"

## 🔄 How It Works

### 1. Market Selection
- Kalshi public API fetches currently open prediction markets
- Markets span multiple categories: politics, economics, sports, tech, climate, entertainment
- System can filter by category or select randomly

### 2. Research Phase
- Claude analyzes the market question and identifies key claims
- Web search uncovers latest information, expert opinions, recent developments
- Evidence is compiled into a research summary

### 3. Council Analysis Phase
- **Parallel Processing**: All three council members analyze simultaneously
- Each member:
  - Reviews the market question and research findings
  - Generates independent probability estimate (0-100%)
  - Lists supporting factors and uncertainties
  - Reports confidence level (low/medium/high)

### 4. Consensus Generation
- Council meeting synthesizes individual analyses
- Identifies areas of strong agreement
- Flags key disagreements and their sources
- Calculates weighted consensus probability
- Assesses overall confidence (0-100%)

### 5. Betting Decision
- **Edge Calculation**: Compares council probability vs market-implied probability
- **Expected Value**: Projects profit/loss if betting at current price
- **Recommendation**: BUY_YES, BUY_NO, or PASS based on edge and confidence
  - **PASS**: If edge is insufficient (< 5%) or confidence is low
  - **BUY_YES**: If council believes YES is underpriced
  - **BUY_NO**: If council believes NO is underpriced

### 6. Execution
- **Dry Run Mode** (Default): Simulates betting without spending money
  - Logs decision details to JSON file
  - Helps validate system before deploying real capital
  - Perfect for backtesting and performance analysis

- **Live Mode** (Optional): Places actual bets on Kalshi
  - Requires authenticated API access
  - Implements proper risk management
  - Tracks portfolio and order status

## 🔑 Key Features

### Multi-Model Consensus
- Leverages three independent analytical perspectives
- Reduces individual model bias through diversity
- Identifies areas of uncertainty through disagreement patterns

### Evidence-Based Research
- Web search integration for current information
- Distinction between facts and narratives
- Source quality validation

### Risk Management
- Conservative bet sizing (starts at $5 per position)
- Edge threshold requirements (minimum 5% edge)
- Confidence score thresholds
- Dry run mode for safe testing

### Comprehensive Logging
- JSON output of all decisions with reasoning
- Market metadata and council analyses
- Expected value calculations
- Execution details for performance tracking

### Extensibility
- Easy to add new council members with different perspectives
- Can integrate additional research sources
- Compatible with advanced betting strategies (Kelly Criterion, etc.)
- Ready for backtesting framework integration

## 📊 Market Categories Available

Through Kalshi, you can analyze prediction markets on:

| Category | Examples |
|----------|----------|
| **Politics** | Elections, policy outcomes, appointments, legislative results |
| **Economics** | Interest rates, inflation, employment, GDP, stock indices |
| **Sports** | Game outcomes, championships, records, draft picks |
| **Technology** | Product launches, IPOs, company valuations, benchmarks |
| **Climate** | Temperature records, weather events, environmental metrics |
| **Entertainment** | Award winners, viewership records, release dates |

## 🛠️ Technical Details

### Authentication

**Public Market Data** (No auth required):
```python
# Fetch markets from public API
response = requests.get(
    "https://api.elections.kalshi.com/trade-api/v2/markets",
    params={"status": "open", "limit": 100}
)
```

**Trading & Portfolio Management** (Auth required):
- RSA signature-based authentication
- 30-minute token expiration (automatic refresh)
- Separate demo and production endpoints

### API Endpoints Used

**Public Endpoints**:
- `GET /markets` - List open/closed markets
- `GET /markets/{ticker}` - Get market details
- `GET /markets/{ticker}/orderbook` - Get orderbook data
- `GET /events/{ticker}` - Get event information
- `GET /series/{ticker}` - Get series information

**Authenticated Endpoints**:
- `POST /portfolio/orders` - Place order
- `GET /portfolio/orders/{order_id}` - Check order status
- `DELETE /portfolio/orders/{order_id}` - Cancel order
- `GET /portfolio` - Get portfolio summary

### Model Configuration

- **Primary Model**: Claude 3.5 Sonnet (claude-3-5-sonnet-20241022)
- **All Council Members**: Use same model for consistency, differ by system prompt
- **Token Budget**: 2000 max tokens per analysis, 1500 for consensus
- **Temperature**: Default 1.0 (not specified in implementation - Claude default)

## 📈 Performance Tracking

The system logs all decisions to JSON files for analysis:

```json
{
  "timestamp": "2025-01-15T14:30:00.123456",
  "market_ticker": "TRUMP-CONV-25",
  "market_title": "Will Trump be convicted...",
  "recommendation": "PASS",
  "consensus_probability": 32,
  "confidence": 67,
  "execution": {
    "status": "passed",
    "reason": "Insufficient edge: 4.0%"
  }
}
```

Track metrics:
- Win rate: % of correct predictions
- ROI: Return on investment
- Calibration: Are 70% probability bets correct ~70% of the time?
- Edge detection: How often does council identify genuine edges?

## ⚠️ Important Disclaimers

### For Testing & Research
- Start with **dry run mode only**
- Never deploy real capital without extensive backtesting
- Test your betting strategy on closed markets first
- Monitor council accuracy over time

### Risk Acknowledgment
- Trading prediction markets involves **real financial risk**
- You can lose some or all invested capital
- Past accuracy ≠ future performance
- Council is an AI system, not a financial advisor

### Before Going Live
1. Run at least 50+ dry run sessions
2. Analyze council accuracy on resolved markets
3. Implement strict position size limits
4. Set daily loss limits
5. Get real financial and legal advice if needed

## 🔮 Future Enhancements

Potential improvements for future versions:

### Analysis Enhancements
- [ ] Add specialized council members for specific domains
- [ ] Implement information source credibility scoring
- [ ] Add historical precedent analysis
- [ ] Incorporate expert consensus data

### Trading Enhancements
- [ ] Implement Kelly Criterion bet sizing
- [ ] Add position correlation analysis
- [ ] Implement stop-loss and take-profit logic
- [ ] Create portfolio rebalancing rules

### Monitoring & Backtesting
- [ ] Build comprehensive backtesting framework
- [ ] Create performance dashboards
- [ ] Implement live portfolio tracking
- [ ] Add Sharpe ratio and drawdown analysis
- [ ] Historical accuracy calibration

### Integration Enhancements
- [ ] Support multiple prediction markets (Polymarket, etc.)
- [ ] Real-time market update webhooks
- [ ] Automated market filtering by expected value
- [ ] Integration with Discord/Slack for alerts

## 📚 Documentation

See `kalshi_llm_council_guide.md` for:
- Complete API documentation
- Detailed authentication setup
- Advanced implementation examples
- Risk management strategies
- Market mechanics explanation

## 🤝 Contributing

This is a template/reference implementation. To extend:

1. **Add council members**: Create new `LLMCouncilMember` instances with different roles
2. **Modify research strategy**: Update `MarketResearcher` prompt engineering
3. **Change betting logic**: Adjust `BettingExecutor` position sizing
4. **Add new data sources**: Extend research findings collection
5. **Implement backtesting**: Use closed markets for validation

## 📞 Support & Resources

- **Kalshi API Docs**: https://docs.kalshi.com
- **Kalshi Help**: https://help.kalshi.com
- **Kalshi Discord**: Community support and dev channel
- **Anthropic API**: https://docs.anthropic.com

## 📄 License

Educational and research purposes. See full disclaimer in code.

---

**Built with**: Anthropic Claude API, Kalshi Prediction Markets API, Python

**Last Updated**: January 2025
