README - Determinants of Global Life Expectancy: A Country-Year Panel Analysis
Student: Nakita Ramachandra Purohit
Mentor: Dr. Md Amir Amiruzzaman
Course: CSC 610 - Independent Research
Date: April 2026

FOLDER CONTENTS
---------------
master_panel.csv          - Cleaned panel dataset (233 countries, 2000-2023)
data_cleaning_merge.py    - Script to clean and merge raw data files
visualizations.py         - Script to generate all 6 figures
regression_models.py      - Script to run OLS regression Models 1, 2, 3
robustness_checks.py      - Script to run pre-2020, trimmed GDP, and VIF checks
verify_stats.py           - Script to verify all numbers reported in the paper
README.txt                - This file

RAW DATA FILES REQUIRED (download separately from sources listed below)
------------------------------------------------------------------------
LE_at_birth.csv                                    - World Bank SP.DYN.LE00.IN
education.csv                                      - World Bank SE.XPD.TOTL.GD.ZS
Health_new.csv                                     - World Bank SH.XPD.CHEX.GD.ZS
pm2_5.csv                                          - World Bank EN.ATM.PM25.MC.M3
life-expectancy-vs-gdp-per-capita.csv              - Our World in Data
life-expectancy-of-women-vs-life-expectancy-of-men.csv - Our World in Data

Data sources:
  World Bank Open Data: https://data.worldbank.org
  Our World in Data:    https://ourworldindata.org

REQUIREMENTS
------------
Python 3.8 or higher

Install required libraries by running:
  pip install pandas numpy matplotlib seaborn scipy statsmodels

HOW TO RUN (in order)
---------------------
Step 1 - Build the master dataset:
  python data_cleaning_merge.py
  Output: master_panel.csv

Step 2 - Verify dataset statistics:
  python verify_stats.py
  Output: printed stats for all 6 figures

Step 3 - Generate visualizations:
  python visualizations.py
  Output: fig1_global_trend.png through fig6_covid_comparison.png

Step 4 - Run regression models:
  python regression_models.py
  Output: printed model results + regression_summary.csv

Step 5 - Run robustness checks:
  python robustness_checks.py
  Output: robustness_results.csv + vif_model3.csv

To save console output as proof:
  python regression_models.py > regression_output.txt
  python robustness_checks.py > robustness_output.txt

IMPORTANT NOTES
---------------
1. All scripts must be run from the same folder as master_panel.csv
2. Run data_cleaning_merge.py FIRST before any other script
3. Raw CSV files must be in the same folder when running Step 1
4. PM2.5 data is only available 2001-2020 (World Bank source limitation)
5. GDP per capita data is only available through 2022 (OWID source limitation)
6. All regression results use HC1 robust standard errors
7. Model 3 is estimated on 2001-2020 subsample due to PM2.5 data availability

REPRODUCIBILITY
---------------
All analysis is fully reproducible from the raw data files.
The master_panel.csv is provided for convenience but can be regenerated
from scratch using data_cleaning_merge.py and the original raw files.
