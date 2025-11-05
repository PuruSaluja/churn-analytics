import pandas as pd
import numpy as np
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants
INPUT_FILE = os.path.join('data', 'intermediate', 'cleaned_data.csv')
OUTPUT_FILE = os.path.join('data', 'processed', 'final_analytical_dataset.csv')

def load_data(filepath):
    logger.info(f"Loading data from {filepath}...")
    return pd.read_csv(filepath)

def create_tenure_cohorts(df):
    """Creates tenure cohorts."""
    logger.info("Creating tenure cohorts...")
    bins = [0, 12, 24, 48, 60, 72, 1000]
    labels = ['0-12 Months', '12-24 Months', '24-48 Months', '48-60 Months', '60-72 Months', '72+ Months']
    df['Tenure_Cohort'] = pd.cut(df['tenure'], bins=bins, labels=labels, right=False)
    return df

def calculate_clv(df):
    """Calculates Customer Lifetime Value (Simple approximation)."""
    logger.info("Calculating CLV...")
    # Simple CLV = MonthlyCharges * Tenure (past value)
    # For predictive CLV, we would need a model, but this is historical value.
    df['Historical_CLV'] = df['MonthlyCharges'] * df['tenure']
    return df

def create_rfm_features(df):
    """Creates RFM-like features."""
    logger.info("Creating RFM features...")
    # Recency: Inverse of Last_Activity_Date (we generated this synthetically)
    # Frequency: Avg_Monthly_Logins
    # Monetary: MonthlyCharges
    
    # We need to parse Last_Activity_Date if it exists
    if 'Last_Activity_Date' in df.columns:
        df['Last_Activity_Date'] = pd.to_datetime(df['Last_Activity_Date'])
        current_date = df['Last_Activity_Date'].max()
        df['Recency_Days'] = (current_date - df['Last_Activity_Date']).dt.days
    
    return df

def create_risk_scores(df):
    """Creates simple risk scores based on heuristics."""
    logger.info("Creating risk scores...")
    
    # 1. Payment Method Risk
    # Electronic check is known to have higher churn
    df['Payment_Risk_Score'] = df['PaymentMethod'].apply(lambda x: 1 if x == 'Electronic check' else 0)
    
    # 2. Contract Risk
    # Month-to-month is high risk
    df['Contract_Risk_Score'] = df['Contract'].apply(lambda x: 1 if x == 'Month-to-month' else 0)
    
    # 3. Support Risk
    # High support tickets = high risk
    if 'Support_Tickets_Opened' in df.columns:
        df['Support_Risk_Score'] = df['Support_Tickets_Opened'].apply(lambda x: 1 if x > 3 else 0)
        
    return df

def main():
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    
    df = load_data(INPUT_FILE)
    
    df = create_tenure_cohorts(df)
    df = calculate_clv(df)
    df = create_rfm_features(df)
    df = create_risk_scores(df)
    
    logger.info(f"Saving feature-engineered data to {OUTPUT_FILE}...")
    df.to_csv(OUTPUT_FILE, index=False)
    logger.info("Feature engineering complete.")

if __name__ == "__main__":
    main()
