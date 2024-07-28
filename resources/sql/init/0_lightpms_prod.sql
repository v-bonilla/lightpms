-- Create the portfolio Management System Database
CREATE DATABASE lightpms_prod;

CREATE USER user_prod PASSWORD '1234'; -- PLEASE CHANGE THE PASSWORD!!!
GRANT USAGE ON SCHEMA public TO user_prod;
GRANT CREATE ON SCHEMA public TO user_prod;
GRANT CONNECT ON DATABASE lightpms_prod TO user_prod;

-- Switch to the PMS Database
\c lightpms_prod;

-- Create the portfolio table
CREATE TABLE portfolio (
    p_id SERIAL PRIMARY KEY,
    p_name VARCHAR(255),
    p_description TEXT,
    p_creation_date DATE
);

-- Create the asset table
CREATE TABLE asset (
    a_id SERIAL PRIMARY KEY,
    a_name VARCHAR(255),
    a_type VARCHAR(255)
);

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

-- Create the MarketData table
CREATE TABLE market_data (
    md_id SERIAL PRIMARY KEY,
    a_id INT REFERENCES asset(a_id),
    md_date DATE,
    md_open_price DECIMAL,
    md_close_price DECIMAL,
    md_volume DECIMAL
);

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
