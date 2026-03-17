# Determinants of Global Life Expectancy (2000–2023)

A reproducible panel data analysis examining which socioeconomic, 
health system, and environmental factors are most strongly associated 
with life expectancy across 233 countries from 2000 to 2023.

## Data Sources
World Bank World Development Indicators(https://data.worldbank.org)
Our World in Data (https://ourworldindata.org)

## Variables
1)Life expectancy at birth (outcome)
2)GDP per capita (log-transformed)
3)Government education expenditure (% GDP)
4)Health expenditure (% GDP)
5)PM2.5 air pollution exposure

## Project Structure
"data_cleaning_merge.py" - data cleaning and merging pipeline
"master_panel.csv" - cleaned panel dataset (5,592 observations)

## Coming Soon
Visualizations (matplotlib, seaborn)
Regression models (OLS, fixed effects)
Results and figures

## Tools Used
Python
pandas
numpy
