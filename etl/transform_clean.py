import pandas as pd
import numpy as np
import os
import logging
from sklearn.preprocessing import LabelEncoder

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants
INPUT_FILE = os.path.join('data', 'raw', 'telco_churn_hybrid.csv')
OUTPUT_FILE = os.path.join('data', 'intermediate', 'cleaned_data.csv')

def load_data(filepath):
    """Loads data from CSV."""
    logger.info(f"Loading data from {filepath}...")
    return pd.read_csv(filepath)

def clean_data(df):
    """Performs data cleaning and standardization."""
    logger.info("Cleaning data...")
    
    # 1. Handle TotalCharges
    # It often contains empty strings " " for new customers. Replace with 0 or MonthlyCharges.
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    df['TotalCharges'] = df['TotalCharges'].fillna(0)
    
    # 2. Standardize Categorical Values
    # 'No internet service' and 'No phone service' can be simplified to 'No' for some columns if preferred,
    # but keeping them distinct is often better for trees. We'll keep them but ensure consistency.
    
    # 3. Encode Binary Columns
    binary_cols = ['Partner', 'Dependents', 'PhoneService', 'PaperlessBilling', 'Churn']
    for col in binary_cols:
        if col in df.columns:
            df[col] = df[col].map({'Yes': 1, 'No': 0})
    
    # Gender
    df['gender'] = df['gender'].map({'Male': 1, 'Female': 0})
    
    # 4. Winsorize Outliers (Optional, but good for linear models)
    # We'll just clip extreme values for MonthlyCharges if needed, but they look bounded in Telco data.
    
    # 5. Fix Data Types
    df['SeniorCitizen'] = df['SeniorCitizen'].astype(int)
    
    return df

def encode_categorical(df):
    """Encodes categorical variables."""
    logger.info("Encoding categorical variables...")
    
    # We will use One-Hot Encoding for multi-class variables for the analytical dataset,
    # but for the intermediate step, we might want to keep them as strings for SQL loading.
    # However, for ML, we need encoding.
    # Strategy: Save a version with strings for SQL/Dashboard, and a version with OHE for ML?
    # The plan says "Encode binary fields" in transform_clean.
    # We will keep multi-class as strings here for better readability in SQL/Dashboard.
    # Feature engineering will handle OHE or Label Encoding for models.
    
    return df

def main():
    # Ensure directory exists
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    
    df = load_data(INPUT_FILE)
    df_clean = clean_data(df)
    df_final = encode_categorical(df_clean)
    
    logger.info(f"Saving cleaned data to {OUTPUT_FILE}...")
    df_final.to_csv(OUTPUT_FILE, index=False)
    logger.info("Data cleaning complete.")

if __name__ == "__main__":
    main()
