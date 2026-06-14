# 🎓 Project Masterclass: Customer Churn Analytics System

## 1. The Business Problem (The "Why")
**Scenario**: A subscription-based Telecom company is losing customers ("churning"). Acquiring a new customer costs 5x more than retaining an existing one.
**Goal**: Build a system to predict *who* will leave and *why*, so the marketing team can intervene.
**Value**: Reducing churn by just 5% can increase profits by 25-95%.

---

## 2. The Solution Architecture (The "How")
We built a modern data stack solution:

### A. Data Engineering (The Foundation)
*   **Ingestion (`ingest_data.py`)**:
    *   We didn't just use the standard Telco dataset. We **enriched** it with synthetic data to make it realistic.
    *   *Key Addition*: Engagement metrics (Login frequency, Support tickets). Real-world churn models *always* use engagement data.
*   **ETL Pipeline**:
    *   **Cleaning**: Handled missing values (e.g., `TotalCharges` for new customers).
    *   **Feature Engineering**: Created "Business Logic" features.
        *   **Tenure Cohorts**: Grouped users (0-12 months, 1-2 years) because behavior changes over time.
        *   **CLV (Customer Lifetime Value)**: `MonthlyCharges * Tenure`. Tells us who is most valuable to save.
        *   **Risk Scores**: Simple heuristics (e.g., "If Month-to-Month AND Electronic Check -> High Risk").

### B. Data Warehousing (The Storage)
*   **Star Schema**: We didn't just dump data into a table. We organized it professionally.
    *   **Fact Tables** (`fact_churn`, `fact_engagement`): Contain the numbers/metrics (events).
    *   **Dimension Tables** (`dim_customer`, `dim_contract`): Contain the descriptive attributes (who/what).
    *   *Why?* This makes SQL queries faster and easier for BI tools like Power BI.

### C. Data Science (The Brains)
*   **Logistic Regression**:
    *   *Purpose*: The "Baseline". It's simple and interpretable.
    *   *Result*: Tells us the *direction* of relationships (e.g., "Higher tenure = Lower churn probability").
*   **XGBoost (Extreme Gradient Boosting)**:
    *   *Purpose*: The "Champion". It captures complex, non-linear patterns (e.g., "High charges only matter if tenure is low").
    *   *Why XGBoost?* It's the industry standard for tabular data competitions and production systems.
*   **SHAP (SHapley Additive exPlanations)**:
    *   *Problem*: XGBoost is a "Black Box". We don't know exactly how it decides.
    *   *Solution*: SHAP values tell us exactly how much each feature contributed to a specific prediction.
    *   *Business Value*: You can tell a support agent, "Offer a discount because this customer's *contract type* is the main issue."

### D. Business Intelligence (The Face)
*   **Dashboard**: Translates complex model outputs into traffic lights (Red/Yellow/Green risk).
*   **Actionable Insights**: We don't just show charts; we show *lists* of customers to call.

---

## 3. Key Interview Talking Points

### "Tell me about a challenging project."
> "I built an end-to-end churn analytics system. I started by engineering a hybrid dataset to simulate real-world engagement signals. I designed a Star Schema warehouse for efficient reporting and trained an XGBoost model that achieved [Score] AUC. I didn't stop at prediction; I used SHAP values to build an explainable dashboard that marketing teams could use to target high-risk segments."

### "How did you handle class imbalance?"
> "Churn is rare (only ~26%). I used the `scale_pos_weight` parameter in XGBoost / `class_weight='balanced'` in Logistic Regression to penalize missing a churner more than missing a non-churner."

### "Why did you choose XGBoost over Random Forest?"
> "XGBoost generally provides better performance on tabular data due to its gradient boosting framework, which iteratively corrects errors of previous trees. It also handles missing values natively."

### "What was your most impactful feature?"
> "The 'Weekly Engagement Score'. It turned out that a drop in login frequency was a leading indicator of churn, often appearing weeks before the customer actually cancelled."

---

## 4. Technical Deep Dive (Files to Know)
*   **`etl/feature_engineering.py`**: Where the "Business Logic" lives. Read the `create_risk_scores` function.
*   **`sql/schema.sql`**: Proof you understand Data Modeling.
*   **`analysis/shap_explainability.ipynb`**: The "Wow" factor. Shows you care about interpretability.
