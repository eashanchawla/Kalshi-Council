from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    market_ticker = Column(String, index=True, nullable=False)
    market_title = Column(String, nullable=False)
    category = Column(String, index=True)
    consensus_probability = Column(Float)
    confidence = Column(Float)
    recommendation = Column(String)
    edge = Column(Float)
    expected_value = Column(Float)
    bet_size = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

    analyses = relationship("CouncilAnalysis", back_populates="prediction")
    snapshots = relationship("MarketSnapshot", back_populates="prediction")
    results = relationship("Result", back_populates="prediction")

    def to_dict(self):
        return {
            "id": self.id,
            "market_ticker": self.market_ticker,
            "market_title": self.market_title,
            "category": self.category,
            "consensus_probability": self.consensus_probability,
            "confidence": self.confidence,
            "recommendation": self.recommendation,
            "edge": self.edge,
            "expected_value": self.expected_value,
            "bet_size": self.bet_size,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

class CouncilAnalysis(Base):
    __tablename__ = "council_analyses"

    id = Column(Integer, primary_key=True, index=True)
    prediction_id = Column(Integer, ForeignKey("predictions.id"), nullable=False)
    member_name = Column(String, nullable=False)
    model_id = Column(String)
    probability = Column(Float)
    confidence = Column(String)
    factors_for = Column(JSON)
    factors_against = Column(JSON)
    reasoning = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    prediction = relationship("Prediction", back_populates="analyses")

    def to_dict(self):
        return {
            "id": self.id,
            "prediction_id": self.prediction_id,
            "member_name": self.member_name,
            "model_id": self.model_id,
            "probability": self.probability,
            "confidence": self.confidence,
            "factors_for": self.factors_for,
            "factors_against": self.factors_against,
            "reasoning": self.reasoning,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

class MarketSnapshot(Base):
    __tablename__ = "market_snapshots"

    id = Column(Integer, primary_key=True, index=True)
    prediction_id = Column(Integer, ForeignKey("predictions.id"), nullable=False)
    yes_price = Column(Float)
    no_price = Column(Float)
    volume = Column(Integer)
    open_interest = Column(Integer)
    close_time = Column(DateTime)
    snapshot_at = Column(DateTime, default=datetime.utcnow)

    prediction = relationship("Prediction", back_populates="snapshots")

    def to_dict(self):
        return {
            "id": self.id,
            "prediction_id": self.prediction_id,
            "yes_price": self.yes_price,
            "no_price": self.no_price,
            "volume": self.volume,
            "open_interest": self.open_interest,
            "close_time": self.close_time.isoformat() if self.close_time else None,
            "snapshot_at": self.snapshot_at.isoformat() if self.snapshot_at else None
        }

class Result(Base):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True, index=True)
    prediction_id = Column(Integer, ForeignKey("predictions.id"), nullable=False)
    resolved_outcome = Column(String) # YES/NO/null
    pnl = Column(Float)
    resolved_at = Column(DateTime, default=datetime.utcnow)

    prediction = relationship("Prediction", back_populates="results")

    def to_dict(self):
        return {
            "id": self.id,
            "prediction_id": self.prediction_id,
            "resolved_outcome": self.resolved_outcome,
            "pnl": self.pnl,
            "resolved_at": self.resolved_at.isoformat() if self.resolved_at else None
        }

# Indexes for performance
Index("ix_council_analyses_prediction_id", CouncilAnalysis.prediction_id)
Index("ix_market_snapshots_prediction_id", MarketSnapshot.prediction_id)
Index("ix_results_prediction_id", Result.prediction_id)
