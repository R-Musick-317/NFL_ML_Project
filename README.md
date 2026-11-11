# NFL Spread Prediction & Betting Model

## Overview
This project aims to identify profitable Expected Value (+EV) betting opportunities against NFL point spreads (BetMGM). By combining an automated machine learning pipeline with a dynamic Power BI visualization layer, this repository predicts NFL spread covers using advanced efficiency metrics. 

The core objective is to exceed the standard Vegas breakeven threshold of **52.38%**, stratifying predictions by the model's confidence level to maximize profitability.

## Project Structure
```text
NFL_ML_Project/
│
├── data/                          # Ignored by Git. Stores exported predictions & tracking logs
│   ├── 2026_week_X_predictions.csv
│   └── model_performance_tracker.csv
│
├── ml_pipeline/                   # Machine Learning scripts & Jupyter notebooks
│   ├── Football ML Test_V2.0.ipynb # Historical backtesting notebook
│   ├── Football ML_Live Prediction.py # Weekly prediction generator
│   └── evaluate_model_performance.py # Automated grading & unit profit tracker
│
├── powerbi_scripts/               # Python transformation scripts executed inside Power BI
│   └── Live Predictions_PBI Upload.py # Ingests latest predictions for Power BI Dim_Team hub
│
├── .gitignore                     # Secures data files and virtual environment artifacts
└── README.md
```

## Machine Learning Pipeline
The predictive model was upgraded from a baseline `LogisticRegression` (50.7% accuracy) to a robust `RandomForestClassifier`, achieving a highly profitable **55.3% accuracy** on strictly out-of-sample testing data.

**Key Features:**
*   **Algorithm:** `RandomForestClassifier` (100 estimators).
*   **Target:** `home_cover` (Binary classification: 1.0 for Home Cover, 0.0 for Away Cover).
*   **Bias Mitigation:** Utilizes `class_weight='balanced'` to correct standard home-field bias, vastly improving the model's recall on away-team covers.
*   **Features:** Uses historical 3-week rolling averages for Offensive Expected Points Added (EPA) and Completion Percentage Over Expected (CPOE).
*   **Data Leakage Prevention:** Uses shifted rolling metrics for training, while applying unshifted 3-game tail averages (`.tail(3)`) for unplayed upcoming matchups.
*   **Confidence Scoring:** Employs `.predict_proba()` to export predictive probability, allowing picks to be ranked and filtered by model confidence tiers.

## Live Predictions & Evaluation Workflows

### 1. Weekly Live Predictions (`Football ML_Live Prediction.py`)
* Automatically detects the immediate upcoming week for the active season in `nflreadpy`.
* Pulls each team's last 3 completed games to establish entering form (handles bye weeks naturally).
* Fits the Random Forest model on all completed historical data (2023–2026) and exports predictions ranked by confidence to `C:\NFL_ML_Project\data`.

### 2. Power BI Transformation (`Live Predictions_PBI Upload.py`)
* Uses Python's `glob` library to dynamically locate and read the newest prediction CSV without requiring hardcoded filenames.
* Transforms each game into dual rows (`Home` and `Away` perspectives) for direct integration into Power BI's `Dim_Team` star-schema data model.

### 3. Automated Performance Evaluation (`evaluate_model_performance.py`)
* Automatically scans all historical weekly prediction files in `data/`.
* Joins picks against completed game scores directly from `nflreadpy` schedules.
* Calculates actual cover outcomes, Win-Loss records, Win %, and financial profit assuming standard -110 juice ($100 risk / $90.91 profit per win).
* Outputs `model_performance_tracker.csv` to feed Power BI profitability dashboards over time.

## Environment Setup
This project runs on a Conda environment (`nfl_env`). To replicate the environment and ensure script integration functions correctly:

1. Create and activate the environment:
   ```bash
   conda create -n nfl_env python=3.10
   conda activate nfl_env
   ```
2. Install dependencies:
   ```bash
   pip install pandas numpy scikit-learn pyarrow nflreadpy matplotlib
   ```
*Note: `matplotlib` is strictly required for Power BI's Python script wrapper to execute successfully.*

## Current Status & Next Steps
*   [x] Establish local Git repository isolated from sync drives.
*   [x] Achieve >52.38% out-of-sample accuracy on holdout data.
*   [x] Export probability/confidence intervals for bet stratification.
*   [x] Build automated live weekly prediction engine (`ml_pipeline/Football ML_Live Prediction.py`).
*   [x] Develop dynamic Power BI prediction upload script (`powerbi_scripts/Live Predictions_PBI Upload.py`).
*   [x] Build automated performance evaluation script (`ml_pipeline/evaluate_model_performance.py`).
*   [ ] Ingest `model_performance_tracker.csv` into Power BI to build live ROI and win-rate dashboards over time.
*   [ ] Build matrix visuals and confidence bucket performance charts in Power BI.