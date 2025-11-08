-- Analytical Views

-- 1. Churn Overview
CREATE VIEW IF NOT EXISTS vw_churn_overview AS
SELECT 
    c.gender,
    c.SeniorCitizen,
    c.Partner,
    c.Dependents,
    ct.Contract,
    ct.Tenure_Cohort,
    p.PaymentMethod,
    ch.Churn,
    ch.Historical_CLV,
    ch.Payment_Risk_Score,
    ch.Contract_Risk_Score
FROM dim_customer c
JOIN dim_contract ct ON c.customerID = ct.customerID
JOIN dim_payment p ON c.customerID = p.customerID
JOIN fact_churn ch ON c.customerID = ch.customerID;

-- 2. High Risk Segments
CREATE VIEW IF NOT EXISTS vw_high_risk_segments AS
SELECT 
    c.customerID,
    ch.Payment_Risk_Score,
    ch.Contract_Risk_Score,
    ch.Support_Risk_Score,
    (ch.Payment_Risk_Score + ch.Contract_Risk_Score + ch.Support_Risk_Score) as Total_Risk_Score
FROM dim_customer c
JOIN fact_churn ch ON c.customerID = ch.customerID
WHERE Total_Risk_Score >= 2;

-- 3. Engagement vs Churn
CREATE VIEW IF NOT EXISTS vw_engagement_vs_churn AS
SELECT 
    e.Weekly_Engagement_Score,
    e.Avg_Monthly_Logins,
    e.Support_Tickets_Opened,
    ch.Churn
FROM fact_engagement e
JOIN fact_churn ch ON e.customerID = ch.customerID;
