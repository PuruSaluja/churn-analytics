-- Data Cleaning & Quality Checks

-- 1. Check for Duplicates
SELECT customerID, COUNT(*) 
FROM dim_customer 
GROUP BY customerID 
HAVING COUNT(*) > 1;

-- 2. Check for Nulls in Critical Fields
SELECT COUNT(*) as Null_Churn_Count 
FROM fact_churn 
WHERE Churn IS NULL;

-- 3. Check for Invalid TotalCharges
SELECT COUNT(*) as Invalid_Charges 
FROM dim_payment 
WHERE TotalCharges < 0;

-- 4. Validate Tenure Consistency
SELECT COUNT(*) as Inconsistent_Tenure
FROM dim_contract c
JOIN fact_engagement e ON c.customerID = e.customerID
WHERE c.Tenure_Cohort = '0-12 Months' AND e.tenure > 12;
