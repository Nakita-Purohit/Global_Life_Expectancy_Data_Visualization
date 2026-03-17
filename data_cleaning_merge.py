# Research: Determinants of Global Life Expectancy

import pandas as pd
import numpy as np

# 1 : Helper function this step cleans the World Bank "wide" format to "long" format

def load_wb(path, value_name):
    """
    Reads a World Bank CSV, skips the 4 junk header rows,
    keeps only Country Code + year columns,
    reshapes from wide to long format.
    """
    df = pd.read_csv(path, skiprows=4, encoding='utf-8-sig')

    # Keeping only the country identifier and year columns (year columns are numeric strings)
    year_cols = [c for c in df.columns if c.isdigit()]
    df = df[['Country Name', 'Country Code'] + year_cols]

    # melting here organizing messy columns into rows to have same format for all data
    df = df.melt(
        id_vars=['Country Name', 'Country Code'],
        var_name='Year',
        value_name=value_name
    )

    df['Year'] = df['Year'].astype(int)
    df[value_name] = pd.to_numeric(df[value_name], errors='coerce')

    return df[['Country Code', 'Year', value_name]]

# 2: Loading & Cleaning each file

#Life Expectancy at Birth (World Bank) outcome is life expectancy at birth, total (years)
le_wb = load_wb('LE_at_birth.csv', 'life_expectancy')

# Education Expenditure (World Bank) outcome is government expenditure on education as % of GD
edu = load_wb('education.csv', 'edu_expenditure_pct_gdp')

#Health Expenditure % GDP (World Bank) outcome is Current health expenditure as % of GDP(indicator: SH.XPD.CHEX.GD.ZS)
health = load_wb('Health_new.csv', 'health_exp_pct_gdp')

# PM2.5 Air Pollution has different format
pm_raw = pd.read_csv('pm2_5.csv', encoding='latin-1')

# This file has TWO indicators stacked keeping only mean annual exposure
pm_raw = pm_raw[pm_raw['Series Name'].str.contains('mean annual', na=False)]

# Year columns in the file look like "2001 [YR2001]" so extracting just the 4-digit year
year_cols = [c for c in pm_raw.columns if 'YR' in c]
pm = pm_raw[['Country Code'] + year_cols].copy()
pm.columns = ['Country Code'] + [c.split(' ')[0] for c in year_cols]  # e.g. "2001"

# again reshaping wide to long
pm = pm.melt(id_vars=['Country Code'], var_name='Year', value_name='pm25')
pm['Year'] = pm['Year'].astype(int)
pm['pm25'] = pd.to_numeric(pm['pm25'], errors='coerce')  # ".." → NaN

# GDP per Capita (Our World in Data)
gdp_raw = pd.read_csv('life-expectancy-vs-gdp-per-capita.csv')

# OWID uses "Code" not "Country Code" like other files so renaming to match World Bank files
gdp = gdp_raw[['Code', 'Year', 'GDP per capita']].rename(columns={
    'Code': 'Country Code',
    'GDP per capita': 'gdp_per_capita'
})

#Life Expectancy by Sex (Our World in Data)
sex_raw = pd.read_csv('life-expectancy-of-women-vs-life-expectancy-of-men.csv')

# Again same renaming "Code" to "Country Code" to match other files
sex = sex_raw[['Code', 'Year', 'Life expectancy of women', 'Life expectancy of men']].rename(columns={
    'Code': 'Country Code',
    'Life expectancy of women': 'le_women',
    'Life expectancy of men': 'le_men'
})

gdp = gdp.dropna(subset=['Country Code'])
sex = sex.dropna(subset=['Country Code'])

# 3: Merging all files into one master Dataset
# Staring Life expectancy as base or backbone here
# then LEeft Join each other variable on Country Code and Year.
# Left Join keeps all LE rows even if other variables are missing for that row.

df = le_wb.copy()

for other_df in [edu, health, pm, gdp, sex]:
    df = df.merge(other_df, on=['Country Code', 'Year'], how='left')


# 4: Filtering to do analysis on samples

# Keeping only 2000–2023
df = df[(df['Year'] >= 2000) & (df['Year'] <= 2023)]

# Remove World Bank aggregate regions (not real countries)
# These codes represent regions/income groups, not individual countries
aggregate_codes = {
    'WLD', 'HIC', 'LIC', 'MIC', 'LMC', 'UMC',
    'EAP', 'ECA', 'LAC', 'MNA', 'NAC', 'SAS', 'SSA',
    'AFE', 'AFW', 'EAR', 'TEA', 'TEC', 'TLA', 'TMN',
    'TSA', 'TSS', 'OSS', 'PSS', 'PST', 'CSS',
    'IBD', 'IBT', 'IDA', 'IDB', 'IDX', 'OED', 'EMU'
}
df = df[df['Country Code'].str.len() == 3]          # ISO codes are only 3 letters
df = df[~df['Country Code'].isin(aggregate_codes)]  # dropping regional aggregates

# STEP 5: Created derived Variables

# Logging transform GDP per capita because GDP ranges from ~$600 to ~$150,000 (very skewed).
# So log scale compresses this range and linearizes the GDP–LE relationship,
# which is standard in economics/epidemiology literature (Preston curve).
df['log_gdp'] = np.log(df['gdp_per_capita'].replace(0, np.nan))

# STEP 6: Last step is reporting and saving
print("=" * 60)
print("MASTER DATASET SUMMARY")
print("=" * 60)
print(f"Total rows    : {len(df):,}")
print(f"Countries     : {df['Country Code'].nunique()}")
print(f"Year range    : {df['Year'].min()} – {df['Year'].max()}")

print("\nFinal columns:")
for col in df.columns:
    print(f"  {col}")

print("\nMissing data (% missing per variable):")
missing = (df.isnull().mean() * 100).round(1)
for col, pct in missing.items():
    flag = " high" if pct > 30 else ""
    print(f"  {col:<30} {pct}%{flag}")

print("\nSample rows — USA:")
print(df[df['Country Code'] == 'USA'].tail(5).to_string(index=False))

# Save final dataset
df.to_csv('master_panel.csv', index=False)
print("\n master_panel.csv saved successfully.")
