-- Initial Migration: 001_initial.sql

CREATE TABLE predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    market_ticker TEXT NOT NULL,
    market_title TEXT NOT NULL,
    category TEXT,
    consensus_probability REAL,
    confidence REAL,
    recommendation TEXT,
    edge REAL,
    expected_value REAL,
    bet_size REAL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX ix_predictions_id ON predictions (id);
CREATE INDEX ix_predictions_market_ticker ON predictions (market_ticker);
CREATE INDEX ix_predictions_category ON predictions (category);

CREATE TABLE council_analyses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prediction_id INTEGER NOT NULL,
    member_name TEXT NOT NULL,
    model_id TEXT,
    probability REAL,
    confidence TEXT,
    factors_for JSON,
    factors_against JSON,
    reasoning TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (prediction_id) REFERENCES predictions (id)
);

CREATE INDEX ix_council_analyses_id ON council_analyses (id);
CREATE INDEX ix_council_analyses_prediction_id ON council_analyses (prediction_id);

CREATE TABLE market_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prediction_id INTEGER NOT NULL,
    yes_price REAL,
    no_price REAL,
    volume INTEGER,
    open_interest INTEGER,
    close_time DATETIME,
    snapshot_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (prediction_id) REFERENCES predictions (id)
);

CREATE INDEX ix_market_snapshots_id ON market_snapshots (id);
CREATE INDEX ix_market_snapshots_prediction_id ON market_snapshots (prediction_id);

CREATE TABLE results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prediction_id INTEGER NOT NULL,
    resolved_outcome TEXT,
    pnl REAL,
    resolved_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (prediction_id) REFERENCES predictions (id)
);

CREATE INDEX ix_results_id ON results (id);
CREATE INDEX ix_results_prediction_id ON results (prediction_id);
