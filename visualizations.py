import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
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
    'HND':'Latin America & Caribbean','JAM':'Latin America & Caribbean',
    'MEX':'Latin America & Caribbean','NIC':'Latin America & Caribbean',
    'PAN':'Latin America & Caribbean','PRY':'Latin America & Caribbean',
    'PER':'Latin America & Caribbean','TTO':'Latin America & Caribbean',
    'URY':'Latin America & Caribbean','VEN':'Latin America & Caribbean',
    'BLZ':'Latin America & Caribbean','GUY':'Latin America & Caribbean',
    'SUR':'Latin America & Caribbean',
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

# Style
plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'font.size': 11,
    'axes.titlesize': 13,
    'axes.titleweight': 'bold',
    'axes.spines.top': False,
    'axes.spines.right': False,
    'figure.dpi': 150
})

COLORS = {
    'main': '#2C6E9E',
    'accent': '#E05C2A',
    'women': '#C0392B',
    'men': '#2980B9',
    'grid': '#E8E8E8'
}

REGION_COLORS = {
    'East Asia & Pacific': '#E74C3C',
    'Europe & Central Asia': '#3498DB',
    'Latin America & Caribbean': '#2ECC71',
    'Middle East & North Africa': '#F39C12',
    'North America': '#9B59B6',
    'South Asia': '#E67E22',
    'Sub-Saharan Africa': '#1ABC9C',
    'Other': '#95A5A6'
}

# Generating here Figure 1: Global Life Expectancy Trend 
fig, ax = plt.subplots(figsize=(10, 5))
global_trend = df.groupby('Year')['life_expectancy'].mean().reset_index()
ax.plot(global_trend['Year'], global_trend['life_expectancy'],
        color=COLORS['main'], linewidth=2.5, zorder=3)
ax.fill_between(global_trend['Year'], global_trend['life_expectancy'],
                alpha=0.12, color=COLORS['main'])
ax.axvspan(2020, 2021.5, alpha=0.12, color=COLORS['accent'], label='COVID-19 period')
ax.axvline(2020, color=COLORS['accent'], linestyle='--', linewidth=1.2, alpha=0.7)
ax.set_xlabel('Year')
ax.set_ylabel('Life Expectancy at Birth (years)')
ax.set_title('Figure 1. Global Average Life Expectancy Trend, 2000–2023')
ax.legend(frameon=False)
ax.yaxis.set_minor_locator(mticker.MultipleLocator(1))
ax.grid(axis='y', color=COLORS['grid'], zorder=0)
ax.set_xlim(2000, 2023)
plt.tight_layout()
# plt.savefig('/mnt/user-data/outputs/fig1_global_trend.png', bbox_inches='tight')
plt.savefig('fig1_global_trend.png', bbox_inches='tight')
plt.close()
print("Figure 1 saved")

# Generating here Figure 2: Life Expectancy by Region 
fig, ax = plt.subplots(figsize=(11, 6))
regions_to_plot = [r for r in REGION_COLORS if r != 'Other']
for region in regions_to_plot:
#     print(df.columns.tolist())
    subset = df[df['region'] == region].groupby('Year')['life_expectancy'].mean()
    ax.plot(subset.index, subset.values,
            label=region, color=REGION_COLORS[region], linewidth=2)
ax.axvline(2020, color='gray', linestyle='--', linewidth=1.2, alpha=0.6, label='2020 (COVID-19)')
ax.set_xlabel('Year')
ax.set_ylabel('Life Expectancy at Birth (years)')
ax.set_title('Figure 2. Life Expectancy Trends by Geographic Region, 2000–2023')
ax.legend(frameon=False, fontsize=9, loc='lower right')
ax.grid(axis='y', color=COLORS['grid'], zorder=0)
ax.set_xlim(2000, 2023)
plt.tight_layout()
# plt.savefig('/mnt/user-data/outputs/fig2_regional_trends.png', bbox_inches='tight')
plt.savefig('fig2_regional_trends.png', bbox_inches='tight')
plt.close()
print("Figure 2 saved")

# Generating here Figure 3: Preston Curve 
fig, ax = plt.subplots(figsize=(10, 6))
scatter_df = df[df['log_gdp'].notna() & df['life_expectancy'].notna()].copy()
regions_present = scatter_df['region'].unique()
for region in regions_present:
    sub = scatter_df[scatter_df['region'] == region]
    color = REGION_COLORS.get(region, '#95A5A6')
    ax.scatter(sub['log_gdp'], sub['life_expectancy'],
               alpha=0.15, s=8, color=color, label=region)
# Fitted line
slope, intercept, r, p, se = stats.linregress(scatter_df['log_gdp'], scatter_df['life_expectancy'])
x_range = np.linspace(scatter_df['log_gdp'].min(), scatter_df['log_gdp'].max(), 200)
ax.plot(x_range, intercept + slope * x_range,
        color='black', linewidth=2, zorder=5, label=f'Fitted line (R²={r**2:.2f})')
ax.set_xlabel('Log GDP per Capita')
ax.set_ylabel('Life Expectancy at Birth (years)')
ax.set_title('Figure 3. Life Expectancy vs. Log GDP per Capita (Preston Curve), 2000–2022')
ax.legend(frameon=False, fontsize=8, markerscale=2)
ax.grid(color=COLORS['grid'], zorder=0)
plt.tight_layout()
# plt.savefig('/mnt/user-data/outputs/fig3_preston_curve.png', bbox_inches='tight')
plt.savefig('fig3_preston_curve.png', bbox_inches='tight')
plt.close()
print("Figure 3 saved")

# Generating here Figure 4: Correlation Heatmap 
fig, ax = plt.subplots(figsize=(9, 7))
corr_vars = ['life_expectancy', 'log_gdp', 'edu_expenditure_pct_gdp',
             'health_exp_pct_gdp', 'pm25']
corr_labels = ['Life Expectancy', 'Log GDP p.c.', 'Education Exp.', 'Health Exp.', 'PM2.5']
corr_df = df[corr_vars].dropna()
print(f"Correlation computed on {len(corr_df)} complete-case observations")
corr_matrix = corr_df.corr()
corr_matrix.index = corr_labels
corr_matrix.columns = corr_labels
mask = np.triu(np.ones_like(corr_matrix, dtype=bool), k=1)
sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='RdBu_r',
            center=0, vmin=-1, vmax=1, ax=ax,
            linewidths=0.5, annot_kws={'size': 11})
ax.set_title('Figure 4. Correlation Heatmap of Key Variables')
plt.tight_layout()
# plt.savefig('/mnt/user-data/outputs/fig4_correlation_heatmap.png', bbox_inches='tight')
plt.savefig('fig4_correlation_heatmap.png', bbox_inches='tight')
plt.close()
print("Figure 4 saved")

# Generating here Figure 5: Women vs Men Life Expectancy
fig, ax = plt.subplots(figsize=(10, 5))
# women_trend = df.groupby('Year')['le_women'].mean()
# men_trend = df.groupby('Year')['le_men'].mean()
sex_df = df.groupby('Year')[['le_women','le_men']].mean().dropna()
women_trend = sex_df['le_women']
men_trend = sex_df['le_men']
ax.plot(women_trend.index, women_trend.values,
        color=COLORS['women'], linewidth=2.5, label='Women')
ax.plot(men_trend.index, men_trend.values,
        color=COLORS['men'], linewidth=2.5, label='Men')
ax.fill_between(women_trend.index, men_trend.values, women_trend.values,
                alpha=0.1, color='purple', label='Gender gap')
ax.axvline(2020, color='gray', linestyle='--', linewidth=1.2, alpha=0.6)
ax.set_xlabel('Year')
ax.set_ylabel('Life Expectancy at Birth (years)')
ax.set_title('Figure 5. Life Expectancy Trends by Sex, 2000–2023')
ax.legend(frameon=False)
ax.grid(axis='y', color=COLORS['grid'], zorder=0)
ax.set_xlim(2000, 2023)
plt.tight_layout()
# plt.savefig('/mnt/user-data/outputs/fig5_sex_comparison.png', bbox_inches='tight')
plt.savefig('fig5_sex_comparison.png', bbox_inches='tight')
plt.close()
print("Figure 5 saved")

# Generating here Figure 6: Pre vs Post 2020 COVID Comparison 
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
pre = df[df['Year'] < 2020]['life_expectancy'].dropna()
post = df[df['Year'] >= 2020]['life_expectancy'].dropna()
axes[0].hist(pre, bins=30, color=COLORS['main'], alpha=0.7, edgecolor='white')
axes[0].axvline(pre.mean(), color=COLORS['accent'], linewidth=2,
                label=f'Mean: {pre.mean():.1f}')
axes[0].set_title('Pre-2020 (2000–2019)')
axes[0].set_xlabel('Life Expectancy (years)')
axes[0].set_ylabel('Frequency')
axes[0].legend(frameon=False)
axes[0].grid(axis='y', color=COLORS['grid'])

axes[1].hist(post, bins=30, color=COLORS['accent'], alpha=0.7, edgecolor='white')
axes[1].axvline(post.mean(), color=COLORS['main'], linewidth=2,
                label=f'Mean: {post.mean():.1f}')
axes[1].set_title('2020–2023 (COVID-19 Period)')
axes[1].set_xlabel('Life Expectancy (years)')
axes[1].set_ylabel('Frequency')
axes[1].legend(frameon=False)
axes[1].grid(axis='y', color=COLORS['grid'])

fig.suptitle('Figure 6. Distribution of Life Expectancy: Pre-2020 vs. 2020–2023',
             fontweight='bold', fontsize=13)
plt.tight_layout()
# plt.savefig('/mnt/user-data/outputs/fig6_covid_comparison.png', bbox_inches='tight')
plt.savefig('fig6_covid_comparison.png', bbox_inches='tight')
plt.close()
print("Figure 6 saved")

print("\n✅ All 6 figures generated successfully!")
