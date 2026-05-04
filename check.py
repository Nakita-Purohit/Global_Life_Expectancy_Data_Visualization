# import pandas as pd

# df = pd.read_csv('master_panel.csv')

# summary = pd.DataFrame({
#     'Missing (%)': (df.isnull().mean()*100).round(2),
#     'Countries with Any Data': [
#         df.groupby('Country Code')[col].count().gt(0).sum() 
#         for col in df.columns
#     ]
# })

# print(summary)
# summary.to_csv('missing_data_summary.csv', index=True)
# ---gpt
# import pandas as pd

# df = pd.read_csv("master_panel.csv")

# # only real variables (exclude identifiers)
# vars_cols = [c for c in df.columns if c not in ["Country Code", "Year"]]

# summary = pd.DataFrame({
#     "Missing (%)": (df[vars_cols].isnull().mean() * 100).round(2),
#     "Countries with >=1 value": [
#         df.groupby("Country Code")[col].apply(lambda s: s.notna().any()).sum()
#         for col in vars_cols
#     ]
# })

# print(summary)
# summary.to_csv("missing_data_summary.csv")

import pandas as pd

df = pd.read_csv('master_panel.csv')

vars_of_interest = ['life_expectancy', 'edu_expenditure_pct_gdp', 
                    'health_exp_pct_gdp', 'pm25', 'gdp_per_capita', 
                    'le_women', 'le_men']

results = []
for col in vars_of_interest:
    # Use variable's own available years as denominator
    available_years = df[df[col].notna()]['Year'].nunique()
    threshold = int(0.8 * available_years)
    
    pct_missing = round(df[col].isnull().mean() * 100, 2)
    any_data = df.groupby('Country Code')[col].count().gt(0).sum()
    full_coverage = df.groupby('Country Code')[col].count().ge(threshold).sum()
    complete = df.groupby('Country Code')[col].count().eq(available_years).sum()
    available_range = f"{df[df[col].notna()]['Year'].min()}–{df[df[col].notna()]['Year'].max()}"
    
    results.append({
        'Variable': col,
        'Years Available': available_range,
        'Missing (%)': pct_missing,
        'Countries (any data)': any_data,
        'Countries (80%+ coverage)': full_coverage,
        'Countries (complete)': complete
    })

out = pd.DataFrame(results)
print(out.to_string(index=False))
out.to_csv('missing_data_summary.csv', index=False)