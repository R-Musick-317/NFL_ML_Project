# NFL Spread Prediction & Betting Model

## Overview
This project aims to identify profitable Expected Value (+EV) betting opportunities against the BetMGM NFL point spread. By combining an automated machine learning pipeline with a dynamic Power BI visualization layer, this repository predicts NFL spread covers using advanced efficiency metrics. 

The core objective is to exceed the standard Vegas breakeven threshold of **52.38%**, stratifying predictions by the model's confidence level to maximize profitability.

## Project Structure
```text
NFL_ML_Project/
│
├── data/                  # Ignored by Git. Stores exported predictions (e.g., 2025_nfl_predictions_with_confidence.csv)
├── ml_pipeline/           # Jupyter notebooks and Python scripts for the core Machine Learning model
├── powerbi_scripts/       # Python extraction scripts used directly within Power BI's Advanced Editor
├── .gitignore             # Secures data files and virtual environment artifacts
└── README.md
```

## Machine Learning Pipeline
The predictive model was upgraded from a baseline `LogisticRegression` (50.7% accuracy) to a robust `RandomForestClassifier`, achieving a highly profitable **55.3% accuracy** on strictly out-of-sample 2025 testing data.

**Key Features:**
*   **Algorithm:** `RandomForestClassifier` (100 estimators).
*   **Target:** `home_cover` (Binary classification: 1.0 for Home Cover, 0.0 for Away Cover).
*   **Bias Mitigation:** Utilizes `class_weight='balanced'` to correct standard home-field bias, vastly improving the model's recall on away-team covers (improved from 29% to 44%).
*   **Features:** Uses strictly historical 3-week rolling averages for Offensive Expected Points Added (EPA) and Completion Percentage Over Expected (CPOE).
*   **Data Leakage Prevention:** Integrates `.shift(1)` logic to ensure predictions are made exclusively using stats available *prior* to kickoff.
*   **Confidence Scoring:** Employs `.predict_proba()` to export the predictive probability of each decision, allowing bets to be filtered by confidence tiers (e.g., >60% conviction).

## Power BI Integration
The repository contains custom Python scripts designed to be executed directly inside Power BI using the `nflreadpy` library. These scripts automatically ingest raw play-by-play and schedule data, format it, and output cleaned tables for visualization.

**Script Capabilities:**
*   **Dynamic Bye-Week Handling:** Uses `.nunique()` on the `week` column to accurately calculate per-game averages without hardcoding divisors.
*   **Data Aggregation:** Pulls Passing/Rushing yards, Points Scored/Allowed, and Turnover Margins.
*   **Stathead Mapping:** Standardizes team abbreviations (e.g., translating 'GB' to 'GNB') to seamlessly join with historical Stathead tables.

## Environment Setup
This project runs on a Conda environment (`nfl_env`). To replicate the environment and ensure Power BI integration functions correctly:

1. Create and activate the environment:
   ```bash
   conda create -n nfl_env python=3.10
   conda activate nfl_env
   ```
2. Install dependencies:
   ```bash
   pip install pandas scikit-learn pyarrow nflreadpy matplotlib
   ```
*Note: `matplotlib` is strictly required for Power BI's Python script wrapper to execute successfully, even if charts are not generated in Python.*

## Current Status & Next Steps
*   [x] Establish local Git repository isolated from OneDrive/Google Drive sync.
*   [x] Achieve >52.38% out-of-sample accuracy on 2025 holdout data.
*   [x] Export probability/confidence intervals for bet stratification.
*   [x] Update historical and current-year Power BI scripts to handle bye-week per-game averages.
*   [ ] Ingest `2025_nfl_predictions_with_confidence.csv` into Power BI.
*   [ ] Build clustered bar charts and matrix visuals to analyze win-rates across different model confidence buckets.
