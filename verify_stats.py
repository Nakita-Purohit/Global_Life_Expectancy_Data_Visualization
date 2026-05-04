import pandas as pd
import numpy as np
from scipy import stats

df = pd.read_csv('master_panel.csv')

region_map = {
    'AFG':'South Asia','BGD':'South Asia','BTN':'South Asia','IND':'South Asia',
    'LKA':'South Asia','MDV':'South Asia','NPL':'South Asia','PAK':'South Asia',
    'AGO':'Sub-Saharan Africa','BEN':'Sub-Saharan Africa','BFA':'Sub-Saharan Africa',
    'BDI':'Sub-Saharan Africa','CMR':'Sub-Saharan Africa','CAF':'Sub-Saharan Africa',
    'TCD':'Sub-Saharan Africa','COM':'Sub-Saharan Africa','COD':'Sub-Saharan Africa',
    'COG':'Sub-Saharan Africa','CIV':'Sub-Saharan Africa','ETH':'Sub-Saharan Africa',
    'GAB':'Sub-Saharan Africa','GMB':'Sub-Saharan Africa','GHA':'Sub-Saharan Africa',
    'GIN':'Sub-Saharan Africa','GNB':'Sub-Saharan Africa','KEN':'Sub-Saharan Africa',
    'LSO':'Sub-Saharan Africa','LBR':'Sub-Saharan Africa','MDG':'Sub-Saharan Africa',
    'MWI':'Sub-Saharan Africa','MLI':'Sub-Saharan Africa','MRT':'Sub-Saharan Africa',
    'MOZ':'Sub-Saharan Africa','NAM':'Sub-Saharan Africa','NER':'Sub-Saharan Africa',
    'NGA':'Sub-Saharan Africa','RWA':'Sub-Saharan Africa','STP':'Sub-Saharan Africa',
    'SEN':'Sub-Saharan Africa','SLE':'Sub-Saharan Africa','SOM':'Sub-Saharan Africa',
    'ZAF':'Sub-Saharan Africa','SSD':'Sub-Saharan Africa','SDN':'Sub-Saharan Africa',
    'SWZ':'Sub-Saharan Africa','TZA':'Sub-Saharan Africa','TGO':'Sub-Saharan Africa',
    'UGA':'Sub-Saharan Africa','ZMB':'Sub-Saharan Africa','ZWE':'Sub-Saharan Africa',
    'MUS':'Sub-Saharan Africa','CPV':'Sub-Saharan Africa','BWA':'Sub-Saharan Africa',
    'ALB':'Europe & Central Asia','ARM':'Europe & Central Asia','AZE':'Europe & Central Asia',
    'BLR':'Europe & Central Asia','BIH':'Europe & Central Asia','GEO':'Europe & Central Asia',
    'KAZ':'Europe & Central Asia','KGZ':'Europe & Central Asia','MDA':'Europe & Central Asia',
    'MNE':'Europe & Central Asia','MKD':'Europe & Central Asia','RUS':'Europe & Central Asia',
    'SRB':'Europe & Central Asia','TJK':'Europe & Central Asia','TKM':'Europe & Central Asia',
    'TUR':'Europe & Central Asia','UKR':'Europe & Central Asia','UZB':'Europe & Central Asia',
    'AUT':'Europe & Central Asia','BEL':'Europe & Central Asia','BGR':'Europe & Central Asia',
    'HRV':'Europe & Central Asia','CYP':'Europe & Central Asia','CZE':'Europe & Central Asia',
    'DNK':'Europe & Central Asia','EST':'Europe & Central Asia','FIN':'Europe & Central Asia',
    'FRA':'Europe & Central Asia','DEU':'Europe & Central Asia','GRC':'Europe & Central Asia',
    'HUN':'Europe & Central Asia','ISL':'Europe & Central Asia','IRL':'Europe & Central Asia',
    'ITA':'Europe & Central Asia','LVA':'Europe & Central Asia','LTU':'Europe & Central Asia',
    'LUX':'Europe & Central Asia','NLD':'Europe & Central Asia','NOR':'Europe & Central Asia',
    'POL':'Europe & Central Asia','PRT':'Europe & Central Asia','ROU':'Europe & Central Asia',
    'SVK':'Europe & Central Asia','SVN':'Europe & Central Asia','ESP':'Europe & Central Asia',
    'SWE':'Europe & Central Asia','CHE':'Europe & Central Asia','GBR':'Europe & Central Asia',
    'DZA':'Middle East & North Africa','BHR':'Middle East & North Africa',
    'EGY':'Middle East & North Africa','IRN':'Middle East & North Africa',
    'IRQ':'Middle East & North Africa','ISR':'Middle East & North Africa',
    'JOR':'Middle East & North Africa','KWT':'Middle East & North Africa',
    'LBN':'Middle East & North Africa','LBY':'Middle East & North Africa',
    'MAR':'Middle East & North Africa','OMN':'Middle East & North Africa',
    'PSE':'Middle East & North Africa','QAT':'Middle East & North Africa',
    'SAU':'Middle East & North Africa','SYR':'Middle East & North Africa',
    'TUN':'Middle East & North Africa','ARE':'Middle East & North Africa',
    'YEM':'Middle East & North Africa',
    'ARG':'Latin America & Caribbean','BOL':'Latin America & Caribbean',
    'BRA':'Latin America & Caribbean','CHL':'Latin America & Caribbean',
    'COL':'Latin America & Caribbean','CRI':'Latin America & Caribbean',
    'CUB':'Latin America & Caribbean','DOM':'Latin America & Caribbean',
    'ECU':'Latin America & Caribbean','SLV':'Latin America & Caribbean',
    'GTM':'Latin America & Caribbean','HTI':'Latin America & Caribbean',
    'HND':'Latin America & Caribbean','MEX':'Latin America & Caribbean',
    'NIC':'Latin America & Caribbean','PAN':'Latin America & Caribbean',
    'PRY':'Latin America & Caribbean','PER':'Latin America & Caribbean',
    'TTO':'Latin America & Caribbean','URY':'Latin America & Caribbean',
    'VEN':'Latin America & Caribbean','BLZ':'Latin America & Caribbean',
    'GUY':'Latin America & Caribbean','SUR':'Latin America & Caribbean',
    'CHN':'East Asia & Pacific','FJI':'East Asia & Pacific',
    'IDN':'East Asia & Pacific','KOR':'East Asia & Pacific',
    'LAO':'East Asia & Pacific','MYS':'East Asia & Pacific',
    'MNG':'East Asia & Pacific','MMR':'East Asia & Pacific',
    'NZL':'East Asia & Pacific','PNG':'East Asia & Pacific',
    'PHL':'East Asia & Pacific','SGP':'East Asia & Pacific',
    'TLS':'East Asia & Pacific','VNM':'East Asia & Pacific',
    'AUS':'East Asia & Pacific','KHM':'East Asia & Pacific',
    'JPN':'East Asia & Pacific','THA':'East Asia & Pacific',
    'USA':'North America','CAN':'North America',
}
df['region'] = df['Country Code'].map(region_map).fillna('Other')

print("Figure 1 Stats")
global_trend = df.groupby('Year')['life_expectancy'].mean()
for yr in [2000, 2019, 2020, 2021, 2022, 2023]:
    print(f"{yr}: {global_trend[yr]:.2f}")

print("\nFigure 2 Regional 2022")
for region in sorted(df['region'].unique()):
    val = df[(df['region']==region)&(df['Year']==2022)]['life_expectancy'].mean()
    n = df[(df['region']==region)&(df['Year']==2022)]['Country Code'].nunique()
    print(f"{region}: {val:.1f} ({n} countries)")

print("\nFigure 3 Preston Curve")
scatter_df = df[df['log_gdp'].notna() & df['life_expectancy'].notna()]
slope, intercept, r, p, se = stats.linregress(scatter_df['log_gdp'], scatter_df['life_expectancy'])
print(f"R²: {r**2:.3f}, Slope: {slope:.3f}, N: {len(scatter_df)}")

print("\nFigure 4 Correlations (complete cases)")
corr_vars = ['life_expectancy','log_gdp','edu_expenditure_pct_gdp','health_exp_pct_gdp','pm25']
corr_df = df[corr_vars].dropna()
print(f"Complete cases used: {len(corr_df)}")
print(corr_df.corr()['life_expectancy'].round(3))

print("\nFigure 5 Sex Stats")
women = df.groupby('Year')['le_women'].mean()
men = df.groupby('Year')['le_men'].mean()
for yr in [2000, 2023]:
    print(f"{yr} — Women: {women[yr]:.1f}, Men: {men[yr]:.1f}, Gap: {women[yr]-men[yr]:.1f}")

print("\nFigure 6 COVID Stats")
pre = df[df['Year']<2020]['life_expectancy'].mean()
post = df[df['Year']>=2020]['life_expectancy'].mean()
print(f"Pre-2020 mean: {pre:.2f}")
print(f"Post-2020 mean: {post:.2f}")