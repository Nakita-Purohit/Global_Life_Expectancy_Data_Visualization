# Determinants of Global Life Expectancy (2000–2023) — Country–Year Panel Study

This project analyzes how key socioeconomic, health-system, and environmental factors are associated with **life expectancy at birth** across countries over time.  
It builds a reproducible **country–year panel dataset** and uses **visual analysis + regression models + robustness checks**.

## What’s inside
- **Dataset construction:** merges World Bank (WDI-style) + OWID (Grapher) CSVs into one `master_panel.csv`
- **Figures (1–6):** global trend, selected region trends, Preston curve, correlation heatmap, women vs men, pre/post-2020 distributions
- **Models (OLS):**
  - Model 1: `life_expectancy ~ log_gdp + Year`
  - Model 2: `+ edu_expenditure_pct_gdp + health_exp_pct_gdp`
  - Model 3: `+ pm25` (restricted to **2001–2020** due to PM2.5 availability)
- **Robustness checks:** pre-2020 re-estimation, GDP trimming (1% tails), VIF

> Note: Results are interpreted as **associations**, not causal effects.

## Data files required (place in project root)
World Bank / WDI-style:
- `LE_at_birth.csv`
- `education.csv`
- `Health_new.csv`
- `pm2_5.csv`

OWID:
- `life-expectancy-vs-gdp-per-capita.csv`
- `life-expectancy-of-women-vs-life-expectancy-of-men.csv`

## How to run (from scratch)
### 1) Install dependencies
```bash
pip install pandas numpy matplotlib statsmodels

**##Run scripts in order**
python data_clean_merge.py
python verify_stats.py
python visualizations.py
python regression_models.py
python robustness_checks.py

Output files generated
master_panel.csv (merged dataset)
fig1_*.png to fig6_*.png (figures)
regression_summary.csv (model fit summary)
robustness_results.csv (robustness summary)
vif_model3.csv (VIF table)

