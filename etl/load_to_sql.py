import pandas as pd
import sqlite3
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants
INPUT_FILE = os.path.join('data', 'processed', 'final_analytical_dataset.csv')
DB_FILE = os.path.join('data', 'processed', 'churn_warehouse.db')
SCHEMA_FILE = os.path.join('sql', 'schema.sql')

def load_data(filepath):
    logger.info(f"Loading data from {filepath}...")
    return pd.read_csv(filepath)

def init_db(db_path, schema_path):
    """Initializes the database with the schema."""
    logger.info(f"Initializing database at {db_path}...")
    conn = sqlite3.connect(db_path)
    with open(schema_path, 'r') as f:
        schema_sql = f.read()
    conn.executescript(schema_sql)
    conn.close()

def load_to_warehouse(df, db_path):
    """Loads data into the star schema tables."""
    logger.info("Loading data into warehouse tables...")
    conn = sqlite3.connect(db_path)
    
    # 1. dim_customer
    dim_customer = df[['customerID', 'gender', 'SeniorCitizen', 'Partner', 'Dependents']].drop_duplicates()
    dim_customer.to_sql('dim_customer', conn, if_exists='replace', index=False)
    
    # 2. dim_contract
    dim_contract = df[['customerID', 'Contract', 'PaperlessBilling', 'Tenure_Cohort']].drop_duplicates()
    dim_contract.to_sql('dim_contract', conn, if_exists='replace', index=False)
    
    # 3. dim_payment
    dim_payment = df[['customerID', 'PaymentMethod', 'MonthlyCharges', 'TotalCharges']].drop_duplicates()
    dim_payment.to_sql('dim_payment', conn, if_exists='replace', index=False)
    
    # 4. fact_subscription
    fact_subscription = df[['customerID', 'PhoneService', 'MultipleLines', 'InternetService', 
                            'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport', 
                            'StreamingTV', 'StreamingMovies']].drop_duplicates()
    fact_subscription.to_sql('fact_subscription', conn, if_exists='replace', index=False)
    
    # 5. fact_engagement
    # Check for columns existence (some might be missing if synthetic gen failed, but it shouldn't)
    engagement_cols = ['customerID', 'tenure', 'Weekly_Engagement_Score', 'Customer_Interactions_Count', 
                       'Support_Tickets_Opened', 'Avg_Monthly_Logins', 'Last_Activity_Date', 
                       'Subscription_History', 'Promo_Usage_Count', 'Acquisition_Channel', 
                       'Customer_Segment', 'Marketing_Touchpoints', 'Recency_Days']
    # Filter only existing columns
    engagement_cols = [c for c in engagement_cols if c in df.columns]
    fact_engagement = df[engagement_cols].drop_duplicates()
    fact_engagement.to_sql('fact_engagement', conn, if_exists='replace', index=False)
    
    # 6. fact_churn
    churn_cols = ['customerID', 'Churn', 'Payment_Risk_Score', 'Contract_Risk_Score', 
                  'Support_Risk_Score', 'Historical_CLV']
    churn_cols = [c for c in churn_cols if c in df.columns]
    fact_churn = df[churn_cols].drop_duplicates()
    fact_churn.to_sql('fact_churn', conn, if_exists='replace', index=False)
    
    conn.close()

def main():
    df = load_data(INPUT_FILE)
    init_db(DB_FILE, SCHEMA_FILE)
    load_to_warehouse(df, DB_FILE)
    logger.info("Data loading complete.")

if __name__ == "__main__":
    main()
