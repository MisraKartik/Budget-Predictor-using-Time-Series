# CPI-Based Household Budget Forecaster

An end-to-end machine learning and time series forecasting project that predicts the **Consumer Price Index (CPI)** for the next six months using three forecasting models and converts those predictions into personalized household budget estimates through an interactive Streamlit application.

---
## Run the app
Click on the link to launch the [streamlit app](https://budgetpredict.streamlit.app/) .

---

## Overview

Inflation reduces purchasing power by increasing the prices of goods and services over time. This project forecasts category-wise Consumer Price Index (CPI) values for the next six months and uses those forecasts to estimate future household budgets.

Rather than simply predicting inflation, the project demonstrates a practical application of data science by helping users understand how inflation may affect their monthly expenses.

---

## Features

- Forecasts CPI for the next six months
- Implements three forecasting models:
  - Ridge Regression
  - SARIMA
  - SARIMAX
- Converts CPI forecasts into projected household budgets
- Interactive Streamlit dashboard
- Category-wise expenditure forecasting
- Multiple visualizations for comparing future expenses
- Compare predictions from three different forecasting models

---

## Project Pipeline

```text
Historical CPI Data
        │
        ▼
Data Collection & Preprocessing
        │
        ▼
Feature Engineering
        │
        ▼
Model Training
 ┌────────┬─────────┬──────────┐
 │ Ridge  │ SARIMA  │ SARIMAX  │
 └────────┴─────────┴──────────┘
        │
        ▼
6-Month CPI Forecasts
        │
        ▼
Budget Projection Engine
        │
        ▼
Interactive Streamlit Dashboard
```

---

## Forecast Categories

The project forecasts CPI for the following expenditure categories:

- Education
- Energy
- Food
- Housing
- Medical
- Transportation

---

## Models Used

### Ridge Regression

Ridge Regression is a regularized linear regression model that minimizes overfitting using L2 regularization while learning long-term trends within CPI data.

**Advantages**

- Handles multicollinearity
- Stable predictions
- Fast training
- Easy to interpret

---

### SARIMA

Seasonal AutoRegressive Integrated Moving Average (SARIMA) captures trend, seasonality, and temporal dependencies present in monthly CPI data.

**Advantages**

- Suitable for seasonal economic data
- Effective for monthly time-series forecasting

---

### SARIMAX

SARIMAX extends SARIMA by incorporating external explanatory variables, allowing additional information to improve forecasting performance when available.

---

## Budget Projection Method

The application converts forecasted CPI values into projected monthly budgets using the following equation:

```text
Projected Budget =
Current Budget × (Forecast CPI / Base CPI)
```

This approach assumes that a user's spending pattern remains constant while adjusting expenditure according to projected inflation.

---

## Dashboard Features

The Streamlit application provides:

- Monthly budget input for each expenditure category
- Separate tabs for Ridge Regression, SARIMA, and SARIMAX forecasts
- Projected budget for each category
- Relative expenditure comparison
- CPI change rankings
- Forecast tables
- Underlying CPI forecasts used in calculations

---

## Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- Statsmodels
- Streamlit
- Altair
- Matplotlib

---

## Applications

This project can be applied to:

- Personal financial planning
- Household budgeting
- Inflation analysis
- Economic forecasting
- Financial technology applications
- Educational demonstrations of time-series forecasting

---


## Learning Outcomes

This project provided practical experience in:

- Time-series forecasting
- Machine learning
- Economic data analysis
- Feature engineering
- Model comparison
- Streamlit application development
- Data visualization
- End-to-end data science workflow

---

