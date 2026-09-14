create database telco_churn;
use telco_churn;

CREATE TABLE customers (
    customerID VARCHAR(20),
    gender VARCHAR(10),
    SeniorCitizen INT,
    Partner VARCHAR(5),
    Dependents VARCHAR(5),
    tenure INT,
    PhoneService VARCHAR(5),
    MultipleLines VARCHAR(20),
    InternetService VARCHAR(20),
    OnlineSecurity VARCHAR(20),
    OnlineBackup VARCHAR(20),
    DeviceProtection VARCHAR(20),
    TechSupport VARCHAR(20),
    StreamingTV VARCHAR(20),
    StreamingMovies VARCHAR(20),
    Contract VARCHAR(20),
    PaperlessBilling VARCHAR(5),
    PaymentMethod VARCHAR(30),
    MonthlyCharges DECIMAL(10,2),
    TotalCharges VARCHAR(20),
    Churn VARCHAR(5)
);

USE telco_churn;
LOAD DATA LOCAL INFILE 'C:/Users/LENOVO/Desktop/New folder (2)/WA_Fn-UseC_-Telco-Customer-Churn.csv'
INTO TABLE customers
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

set global local_infile = 1;


select * from customers;
select count(*) from customers;

select * from customers limit 5;

# BlanK Values(Total Charges)

select count(*) from customers where trim(TotalCharges)= '';

ALTER TABLE customers ADD COLUMN TotalCharges_clean DECIMAL(10,2);

UPDATE customers
SET TotalCharges_clean = CASE
    WHEN TRIM(TotalCharges) = '' THEN NULL
    ELSE CAST(TotalCharges AS DECIMAL(10,2))
END;

SELECT COUNT(*) AS total_rows,
       COUNT(TotalCharges_clean) AS non_null,
       SUM(CASE WHEN TotalCharges_clean IS NULL THEN 1 ELSE 0 END) AS nulls
FROM customers;


#First Churn Rate View
SELECT
    Contract,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct
FROM customers
GROUP BY Contract
ORDER BY churn_rate_pct DESC;


select distinct Churn,length(Churn) from customers;

UPDATE customers
SET Churn = TRIM(Churn);

SELECT DISTINCT Churn, LENGTH(Churn) FROM customers;

SELECT
    Contract,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct
FROM customers
GROUP BY Contract
ORDER BY churn_rate_pct DESC;

SELECT DISTINCT Churn, LENGTH(Churn), HEX(Churn) FROM customers;

UPDATE customers
SET Churn = REPLACE(REPLACE(Churn, CHAR(13), ''), CHAR(10), '');

SELECT DISTINCT Churn, LENGTH(Churn) FROM customers;

SELECT
    Contract,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct
FROM customers
GROUP BY Contract
ORDER BY churn_rate_pct DESC;


SELECT
    CASE
        WHEN tenure <= 12 THEN '0-12 months'
        WHEN tenure <= 24 THEN '13-24 months'
        WHEN tenure <= 48 THEN '25-48 months'
        ELSE '49+ months'
    END AS tenure_bucket,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct
FROM customers
GROUP BY tenure_bucket
ORDER BY MIN(tenure);

SELECT
    SUM(CASE WHEN Churn = 'Yes' THEN TotalCharges_clean ELSE 0 END) AS revenue_lost_to_churn,
    SUM(TotalCharges_clean) AS total_revenue,
    ROUND(100.0 * SUM(CASE WHEN Churn = 'Yes' THEN TotalCharges_clean ELSE 0 END) / SUM(TotalCharges_clean), 2) AS pct_revenue_at_risk
FROM customers
GROUP BY NULL;