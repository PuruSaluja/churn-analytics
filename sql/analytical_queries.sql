-- Advanced Analytical Queries

-- 1. Cohort Retention Analysis (Churn Rate by Tenure Cohort)
SELECT 
    Tenure_Cohort,
    COUNT(customerID) as Total_Customers,
    SUM(Churn) as Churned_Customers,
    ROUND(CAST(SUM(Churn) AS FLOAT) / COUNT(customerID) * 100, 2) as Churn_Rate_Percent
FROM vw_churn_overview
GROUP BY Tenure_Cohort
ORDER BY Tenure_Cohort;

-- 2. CLV by Churn Risk
SELECT 
    Churn,
    ROUND(AVG(Historical_CLV), 2) as Avg_CLV,
    ROUND(SUM(Historical_CLV), 2) as Total_CLV
FROM vw_churn_overview
GROUP BY Churn;

-- 3. High Risk Payment Method Analysis
SELECT 
    PaymentMethod,
    COUNT(customerID) as Total_Customers,
    SUM(Churn) as Churned_Customers,
    ROUND(CAST(SUM(Churn) AS FLOAT) / COUNT(customerID) * 100, 2) as Churn_Rate_Percent
FROM vw_churn_overview
GROUP BY PaymentMethod
ORDER BY Churn_Rate_Percent DESC;

-- 4. Engagement Score Correlation with Churn
SELECT 
    CASE 
        WHEN Weekly_Engagement_Score >= 8 THEN 'High Engagement'
        WHEN Weekly_Engagement_Score >= 5 THEN 'Medium Engagement'
        ELSE 'Low Engagement'
    END as Engagement_Level,
    COUNT(*) as Count,
    SUM(Churn) as Churned,
    ROUND(CAST(SUM(Churn) AS FLOAT) / COUNT(*) * 100, 2) as Churn_Rate
FROM vw_engagement_vs_churn
GROUP BY 1
ORDER BY Churn_Rate DESC;
