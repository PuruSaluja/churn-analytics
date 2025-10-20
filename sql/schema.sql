-- Star Schema for Customer Churn Analytics

-- Dimension: Customer
CREATE TABLE IF NOT EXISTS dim_customer (
    customerID TEXT PRIMARY KEY,
    gender TEXT,
    SeniorCitizen INTEGER,
    Partner INTEGER,
    Dependents INTEGER
);

-- Dimension: Contract
CREATE TABLE IF NOT EXISTS dim_contract (
    customerID TEXT PRIMARY KEY,
    Contract TEXT,
    PaperlessBilling INTEGER,
    Tenure_Cohort TEXT,
    FOREIGN KEY (customerID) REFERENCES dim_customer(customerID)
);

-- Dimension: Payment
CREATE TABLE IF NOT EXISTS dim_payment (
    customerID TEXT PRIMARY KEY,
    PaymentMethod TEXT,
    MonthlyCharges REAL,
    TotalCharges REAL,
    FOREIGN KEY (customerID) REFERENCES dim_customer(customerID)
);

-- Fact: Subscription Services
CREATE TABLE IF NOT EXISTS fact_subscription (
    customerID TEXT PRIMARY KEY,
    PhoneService INTEGER,
    MultipleLines TEXT,
    InternetService TEXT,
    OnlineSecurity TEXT,
    OnlineBackup TEXT,
    DeviceProtection TEXT,
    TechSupport TEXT,
    StreamingTV TEXT,
    StreamingMovies TEXT,
    FOREIGN KEY (customerID) REFERENCES dim_customer(customerID)
);

-- Fact: Engagement & Behavior (Synthetic Features)
CREATE TABLE IF NOT EXISTS fact_engagement (
    customerID TEXT PRIMARY KEY,
    tenure INTEGER,
    Weekly_Engagement_Score REAL,
    Customer_Interactions_Count INTEGER,
    Support_Tickets_Opened INTEGER,
    Avg_Monthly_Logins INTEGER,
    Last_Activity_Date TEXT,
    Subscription_History TEXT,
    Promo_Usage_Count INTEGER,
    Acquisition_Channel TEXT,
    Customer_Segment TEXT,
    Marketing_Touchpoints INTEGER,
    Recency_Days INTEGER,
    FOREIGN KEY (customerID) REFERENCES dim_customer(customerID)
);

-- Fact: Churn & Risk
CREATE TABLE IF NOT EXISTS fact_churn (
    customerID TEXT PRIMARY KEY,
    Churn INTEGER,
    Payment_Risk_Score INTEGER,
    Contract_Risk_Score INTEGER,
    Support_Risk_Score INTEGER,
    Historical_CLV REAL,
    FOREIGN KEY (customerID) REFERENCES dim_customer(customerID)
);
