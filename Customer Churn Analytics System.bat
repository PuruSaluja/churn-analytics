@echo off
echo ==========================================
echo Customer Churn Analytics System - Pipeline
echo ==========================================

echo [1/4] Ingesting Data...
python etl/ingest_data.py
if %errorlevel% neq 0 (
    echo Error in Data Ingestion.
    pause
    exit /b %errorlevel%
)

echo [2/4] Cleaning & Transforming...
python etl/transform_clean.py
if %errorlevel% neq 0 (
    echo Error in Transformation.
    pause
    exit /b %errorlevel%
)

echo [3/4] Feature Engineering...
python etl/feature_engineering.py
if %errorlevel% neq 0 (
    echo Error in Feature Engineering.
    pause
    exit /b %errorlevel%
)

echo [4/4] Loading to SQL Warehouse...
python etl/load_to_sql.py
if %errorlevel% neq 0 (
    echo Error in SQL Loading.
    pause
    exit /b %errorlevel%
)

echo ==========================================
echo Pipeline Completed Successfully!
echo Data is ready in data/processed/
echo ==========================================
pause
