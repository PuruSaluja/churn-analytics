import pandas as pd
import numpy as np
import requests
import os
import logging
from faker import Faker
import random
from datetime import datetime, timedelta

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants
DATA_DIR = os.path.join('data', 'raw')
TELCO_URL = "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv"
OUTPUT_FILE = os.path.join(DATA_DIR, 'telco_churn_hybrid.csv')
SYNTHETIC_COUNT = 10000  # Number of synthetic records to generate

def download_telco_data(url, save_path):
    """Downloads the Telco Customer Churn dataset."""
    try:
        logger.info(f"Downloading data from {url}...")
        response = requests.get(url)
        response.raise_for_status()
        
        # Save temporarily to load into pandas
        temp_path = os.path.join(DATA_DIR, 'temp_telco.csv')
        with open(temp_path, 'wb') as f:
            f.write(response.content)
            
        df = pd.read_csv(temp_path)
        logger.info(f"Successfully downloaded {len(df)} records.")
        os.remove(temp_path)
        return df
    except Exception as e:
        logger.error(f"Failed to download data: {e}")
        # Fallback: Generate synthetic Telco-like data if download fails
        logger.warning("Generating synthetic Telco data as fallback...")
        return generate_synthetic_telco_data(7043)

def generate_synthetic_telco_data(n_rows):
    """Generates synthetic data mimicking the Telco dataset structure."""
    fake = Faker()
    data = []
    for _ in range(n_rows):
        data.append({
            'customerID': fake.uuid4()[:8],
            'gender': random.choice(['Male', 'Female']),
            'SeniorCitizen': random.choice([0, 1]),
            'Partner': random.choice(['Yes', 'No']),
            'Dependents': random.choice(['Yes', 'No']),
            'tenure': random.randint(0, 72),
            'PhoneService': random.choice(['Yes', 'No']),
            'MultipleLines': random.choice(['No phone service', 'No', 'Yes']),
            'InternetService': random.choice(['DSL', 'Fiber optic', 'No']),
            'OnlineSecurity': random.choice(['No', 'Yes', 'No internet service']),
            'OnlineBackup': random.choice(['No', 'Yes', 'No internet service']),
            'DeviceProtection': random.choice(['No', 'Yes', 'No internet service']),
            'TechSupport': random.choice(['No', 'Yes', 'No internet service']),
            'StreamingTV': random.choice(['No', 'Yes', 'No internet service']),
            'StreamingMovies': random.choice(['No', 'Yes', 'No internet service']),
            'Contract': random.choice(['Month-to-month', 'One year', 'Two year']),
            'PaperlessBilling': random.choice(['Yes', 'No']),
            'PaymentMethod': random.choice(['Electronic check', 'Mailed check', 'Bank transfer (automatic)', 'Credit card (automatic)']),
            'MonthlyCharges': round(random.uniform(18.25, 118.75), 2),
            'TotalCharges': ' ', # Will be calculated later or left as space for cleaning
            'Churn': random.choice(['Yes', 'No'])
        })
    df = pd.DataFrame(data)
    # Fix TotalCharges roughly
    df['TotalCharges'] = df.apply(lambda x: str(round(x['MonthlyCharges'] * x['tenure'], 2)) if x['tenure'] > 0 else ' ', axis=1)
    return df

def generate_advanced_features(df):
    """Generates advanced synthetic features for the dataset."""
    logger.info("Generating advanced synthetic features...")
    fake = Faker()
    
    # Ensure reproducibility
    Faker.seed(42)
    random.seed(42)
    np.random.seed(42)
    
    n = len(df)
    
    # 1. Weekly Engagement Score (0-10)
    # Higher for non-churners, lower for churners
    df['Weekly_Engagement_Score'] = np.random.normal(loc=6, scale=2, size=n)
    df.loc[df['Churn'] == 'Yes', 'Weekly_Engagement_Score'] -= 2 # Lower engagement for churners
    df['Weekly_Engagement_Score'] = df['Weekly_Engagement_Score'].clip(0, 10).round(1)
    
    # 2. Number of Interactions (Customer Service calls, etc.)
    df['Customer_Interactions_Count'] = np.random.poisson(lam=2, size=n)
    df.loc[df['Churn'] == 'Yes', 'Customer_Interactions_Count'] += 2 # More complaints for churners
    
    # 3. Support Tickets Opened (Last 12 months)
    df['Support_Tickets_Opened'] = np.random.poisson(lam=1, size=n)
    df.loc[df['Churn'] == 'Yes', 'Support_Tickets_Opened'] += 2
    
    # 4. Monthly Login Frequency
    df['Avg_Monthly_Logins'] = np.random.randint(1, 30, size=n)
    df.loc[df['Churn'] == 'Yes', 'Avg_Monthly_Logins'] = df.loc[df['Churn'] == 'Yes', 'Avg_Monthly_Logins'] * 0.5 # Less frequent logins
    df['Avg_Monthly_Logins'] = df['Avg_Monthly_Logins'].round(0).astype(int)
    
    # 5. Last Activity Timestamp
    # Generate random dates within last 30 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    def random_date(start, end):
        return start + timedelta(seconds=random.randint(0, int((end - start).total_seconds())))
        
    df['Last_Activity_Date'] = [random_date(start_date, end_date) for _ in range(n)]
    
    # 6. Subscription Upgrades/Downgrades
    df['Subscription_History'] = np.random.choice(['No Change', 'Upgraded', 'Downgraded'], size=n, p=[0.8, 0.1, 0.1])
    
    # 7. Promo Usage
    df['Promo_Usage_Count'] = np.random.randint(0, 5, size=n)
    
    # 8. Acquisition Channel
    df['Acquisition_Channel'] = np.random.choice(['Organic', 'Paid Search', 'Social Media', 'Referral', 'Affiliate'], size=n)
    
    # 9. Customer Segment (Silver/Gold/Platinum)
    # Based roughly on MonthlyCharges
    conditions = [
        (df['MonthlyCharges'] < 50),
        (df['MonthlyCharges'] >= 50) & (df['MonthlyCharges'] < 90),
        (df['MonthlyCharges'] >= 90)
    ]
    choices = ['Silver', 'Gold', 'Platinum']
    df['Customer_Segment'] = np.select(conditions, choices, default='Silver')
    
    # 10. Marketing Touchpoint Count
    df['Marketing_Touchpoints'] = np.random.randint(1, 15, size=n)
    
    return df

def main():
    # Ensure directory exists
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # 1. Get Base Data (Telco)
    df_telco = download_telco_data(TELCO_URL, OUTPUT_FILE)
    
    # 2. Generate Additional Synthetic Records (to reach ~20k total if needed, or just enrich)
    # The user asked to "Generate 10k–20k synthetic records if needed and merge"
    # Telco is ~7k. Let's generate 13k more to reach 20k.
    n_synthetic = 20000 - len(df_telco)
    if n_synthetic > 0:
        logger.info(f"Generating {n_synthetic} additional synthetic records to reach 20k total...")
        df_synthetic = generate_synthetic_telco_data(n_synthetic)
        df_combined = pd.concat([df_telco, df_synthetic], ignore_index=True)
    else:
        df_combined = df_telco
        
    # 3. Add Advanced Features to ALL records
    df_final = generate_advanced_features(df_combined)
    
    # 4. Save
    logger.info(f"Saving final hybrid dataset with {len(df_final)} records to {OUTPUT_FILE}...")
    df_final.to_csv(OUTPUT_FILE, index=False)
    logger.info("Data ingestion complete.")

if __name__ == "__main__":
    main()
