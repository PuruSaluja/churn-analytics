# Dashboard Instructions - Customer Churn Analytics

## Overview
This document provides step-by-step instructions to build the interactive dashboard using Power BI or Tableau. The dashboard is designed to provide executive-level insights into customer churn, identifying high-risk segments and actionable opportunities.

## Data Source
- **File**: `dashboard/export_dataset_for_dashboard.csv`
- **Type**: CSV
- **Key Fields**: `Churn` (Target), `Tenure_Cohort`, `MonthlyCharges`, `Weekly_Engagement_Score`, `Payment_Risk_Score`, `Historical_CLV`.

## Page 1: Executive Summary
**Goal**: High-level overview of churn health.
- **KPI Cards**:
    - **Overall Churn Rate**: (Count of Churn='Yes' / Total Customers) %
    - **Total Customers**: Count of `customerID`
    - **Total Monthly Revenue**: Sum of `MonthlyCharges`
    - **Revenue at Risk**: Sum of `MonthlyCharges` where Churn='Yes' (or predicted high risk)
- **Charts**:
    - **Churn Trend (if date available)** or **Churn by Contract Type** (Donut Chart).
    - **Churn by Tenure Cohort** (Bar Chart): Show that early tenure has highest churn.
    - **Churn by Payment Method** (Horizontal Bar Chart).

## Page 2: Churn Drivers & Risk Analysis
**Goal**: Understand *why* customers are leaving.
- **Charts**:
    - **Engagement vs. Churn** (Box Plot or Violin Plot): `Weekly_Engagement_Score` by `Churn`.
    - **Support Tickets vs. Churn** (Bar Chart): Average tickets for Churn vs. Non-Churn.
    - **Monthly Charges Distribution** (Histogram): Overlay Churn vs. Non-Churn.
    - **Risk Score Heatmap**: `Contract_Risk_Score` vs. `Payment_Risk_Score` colored by Churn Rate.

## Page 3: Segmentation & Cohorts
**Goal**: Deep dive into customer segments.
- **Charts**:
    - **Customer Segments Profile** (Table/Matrix): Avg Tenure, Avg Charges, Churn Rate per Segment (Silver/Gold/Platinum).
    - **Retention Cohort Analysis** (Heatmap): If time-series data is simulated, show retention over months. Otherwise, use Tenure Cohorts as proxy.
    - **CLV by Segment** (Bar Chart): Average `Historical_CLV` by Segment.

## Page 4: Predictive Insights (Actionable)
**Goal**: List of customers to target.
- **Table**: "High Risk Customer List"
    - Columns: `customerID`, `Tenure`, `MonthlyCharges`, `Engagement_Score`, `Risk_Level` (High/Medium/Low).
    - Filter: Show only active customers (Churn='No') with High Risk characteristics (e.g., Low Engagement, Month-to-Month).
- **Slicers/Filters**:
    - Contract Type
    - Payment Method
    - Tenure Cohort

## Color Palette (Professional)
- **Primary**: Navy Blue (`#003f5c`)
- **Secondary**: Teal (`#2f4b7c`)
- **Accent (Churn/Risk)**: Coral/Red (`#ff7c43`)
- **Neutral**: Light Gray (`#f1f1f1`)

## DAX Formulas (Power BI Examples)
```dax
Churn Rate = DIVIDE(CALCULATE(COUNTROWS(Table), Table[Churn] = 1), COUNTROWS(Table))

Revenue at Risk = CALCULATE(SUM(Table[MonthlyCharges]), Table[Churn] = 1)

High Risk Count = CALCULATE(COUNTROWS(Table), Table[Payment_Risk_Score] = 1, Table[Contract_Risk_Score] = 1)
```
