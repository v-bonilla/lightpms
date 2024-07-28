-- Create the portfolio Management System Database
CREATE DATABASE lightpms_dev;

CREATE USER user_dev PASSWORD 'ue3r_deV';
GRANT USAGE ON SCHEMA public TO user_dev;
GRANT CREATE ON SCHEMA public TO user_dev;
GRANT CONNECT ON DATABASE lightpms_dev TO user_dev;


-- Switch to the PMS Database
\c lightpms_dev;

-- Create the portfolio table
CREATE TABLE portfolio (
    p_id SERIAL PRIMARY KEY,
    p_name VARCHAR(255),
    p_description TEXT,
    p_creation_date DATE
);

INSERT INTO portfolio (p_name, p_description, p_creation_date)
VALUES
('portfolio_test_1', 'First testing portfolio.', '2023-01-01'),
('portfolio_test_2', 'Second testing portfolio.', '2023-04-01');

-- Create the asset table
CREATE TABLE asset (
    a_id SERIAL PRIMARY KEY,
    a_name VARCHAR(255),
    a_type VARCHAR(255)
);

INSERT INTO asset (a_name, a_type)
VALUES
('BTCUSD', 'perpetual'),
('ETHUSD', 'perpetual'),
('ARBUSD', 'perpetual');

-- Create the Transaction table
CREATE TABLE transaction (
    t_id SERIAL PRIMARY KEY,
    p_id INT REFERENCES portfolio(p_id),
    a_id INT REFERENCES asset(a_id),
    t_date DATE,
    t_type VARCHAR(10),
    t_quantity DECIMAL,
    t_price DECIMAL
);

INSERT INTO transaction (p_id, a_id, t_date, t_type, t_quantity, t_price)
VALUES
-- Portfolio 1
-- BTCUSD long. Realized PnL -6,000 USD
(1, 1, '2023-01-01', 'buy', 1.0, 10000.0),
(1, 1, '2023-01-03', 'sell', 0.5, 8000.0),
-- ETHUSD long. Realized PnL +20 USD
(1, 2, '2023-01-02', 'buy', 0.1, 1000.0),
(1, 2, '2023-01-05', 'sell', 0.01, 2000.0),
-- ARBUSD long. Realized PnL +50 USD
(2, 3, '2023-01-02', 'buy', 10000.0, 0.01),
(2, 3, '2023-01-03', 'sell', 10000.0, 0.015),
-- Portfolio 2
-- BTCUSD short. Realized PnL +100,000 USD
(2, 1, '2023-04-01', 'sell', 10.0, 20000.0),
(2, 1, '2023-04-05', 'buy', 10.0, 10000.0),
-- ARBUSD short. Realized PnL -50 USD
(2, 3, '2023-04-02', 'short', 10000.0, 0.01),
(2, 3, '2023-04-03', 'buy', 10000.0, 0.015);
-- ETHUSD short. Realized PnL -20 USD
(1, 2, '2023-04-02', 'sell', 0.1, 1000.0),
(1, 2, '2023-04-05', 'buy', 0.01, 2000.0),

-- Create the MarketData table
CREATE TABLE market_data (
    md_id SERIAL PRIMARY KEY,
    a_id INT REFERENCES asset(a_id),
    md_date DATE,
    md_open_price DECIMAL,
    md_close_price DECIMAL,
    md_volume DECIMAL
);

INSERT INTO market_data (a_id, md_date, md_close_price)
VALUES
-- BTCUSD
(1, '2023-01-01', 11000.0),
(1, '2023-01-02', 12000.0),
(1, '2023-01-03', 6000.0),
(1, '2023-04-01', 19000.0),
(1, '2023-04-02', 20000.0),
(1, '2023-04-03', 19000.0),
(1, '2023-04-04', 15000.0),
(1, '2023-04-05', 12000.0),
-- ETHUSD
(2, '2023-01-02', 1100.0),
(2, '2023-01-03', 1600.0),
(2, '2023-01-04', 2200.0),
(2, '2023-01-05', 1900.0),
(2, '2023-04-02', 1100.0),
(2, '2023-04-03', 1600.0),
(2, '2023-04-04', 2200.0),
(2, '2023-04-05', 1900.0),
-- ARBUSD
(3, '2023-01-02', 0.011),
(3, '2023-01-03', 0.02),
(3, '2023-04-02', 0.011),
(3, '2023-04-03', 0.02);

-- Create the Benchmark table
CREATE TABLE benchmark (
    b_id SERIAL PRIMARY KEY,
    b_name VARCHAR(255),
    b_type VARCHAR(255)
);

-- Create the BenchmarkData table
CREATE TABLE benchmark_data (
    bd_id SERIAL PRIMARY KEY,
    b_id INT REFERENCES benchmark(b_id),
    bd_date DATE,
    bd_value DECIMAL
);

-- Create the RiskMetrics table
CREATE TABLE risk_metrics (
    rm_id SERIAL PRIMARY KEY,
    p_id INT REFERENCES portfolio(p_id),
    rm_date DATE,
    rm_var95 DECIMAL,
    rm_var99 DECIMAL,
    rm_std DECIMAL,
    rm_beta DECIMAL
);

-- Create the PortfolioAsset intersection table for the Many-to-Many relationship between portfolio and asset
CREATE TABLE portfolio_asset (
    p_id INT REFERENCES portfolio(p_id),
    a_id INT REFERENCES asset(a_id),
    pa_quantity DECIMAL,
    PRIMARY KEY (p_id, a_id)
);

INSERT INTO portfolio_asset (p_id, a_id, pa_quantity)
VALUES
-- Portfolio 1
(1, 1, 0.5),
(1, 2, 0.9),
-- Portfolio 2
(2, 2, 0.9);
