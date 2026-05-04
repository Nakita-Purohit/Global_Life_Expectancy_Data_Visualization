from statsmodels.stats.outliers_influence import variance_inflation_factor
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import warnings
warnings.filterwarnings('ignore')

#  Load the Data
df = pd.read_csv('master_panel.csv')

print("=" * 65)
print("REGRESSION ANALYSIS: DETERMINANTS OF GLOBAL LIFE EXPECTANCY")
print("=" * 65)

# MODEL 1: Baseline is LE vs log GDP plus Year
# Only countries with log_gdp data
m1_data = df[['Country Code', 'life_expectancy', 'log_gdp', 'Year']].dropna()

model1 = smf.ols(
    'life_expectancy ~ log_gdp + Year',
    data=m1_data
).fit(cov_type='HC1')  # robust standard errors

print("\n" + "=" * 65)
print("MODEL 1: Baseline (Life Expectancy ~ Log GDP + Year)")
print(
    f"Observations: {int(model1.nobs):,} | Countries: {m1_data['Country Code'].nunique()}")
print("=" * 65)
print(f"{'Variable':<30} {'Coef':>8} {'Std Err':>10} {'p-value':>10}")
print("-" * 65)
for var in ['Intercept', 'log_gdp', 'Year']:
    coef = model1.params[var]
    se = model1.bse[var]
    pval = model1.pvalues[var]
    stars = '***' if pval < 0.01 else '**' if pval < 0.05 else '*' if pval < 0.1 else ''
    print(f"{var:<30} {coef:>8.3f} {se:>10.3f} {pval:>10.4f} {stars}")
print(f"\nR²: {model1.rsquared:.3f} | Adj. R²: {model1.rsquared_adj:.3f}")

# MODEL 2: Add Education plus Health Expenditure

m2_data = df[['Country Code', 'life_expectancy', 'log_gdp', 'Year',
              'edu_expenditure_pct_gdp', 'health_exp_pct_gdp']].dropna()

model2 = smf.ols(
    'life_expectancy ~ log_gdp + Year + edu_expenditure_pct_gdp + health_exp_pct_gdp',
    data=m2_data
).fit(cov_type='HC1')

print("\n" + "=" * 65)
print("MODEL 2: + Education + Health Expenditure")
print(
    f"Observations: {int(model2.nobs):,} | Countries: {m2_data['Country Code'].nunique()}")
print("=" * 65)
print(f"{'Variable':<30} {'Coef':>8} {'Std Err':>10} {'p-value':>10}")
print("-" * 65)
for var in ['Intercept', 'log_gdp', 'Year', 'edu_expenditure_pct_gdp', 'health_exp_pct_gdp']:
    coef = model2.params[var]
    se = model2.bse[var]
    pval = model2.pvalues[var]
    stars = '***' if pval < 0.01 else '**' if pval < 0.05 else '*' if pval < 0.1 else ''
    print(f"{var:<30} {coef:>8.3f} {se:>10.3f} {pval:>10.4f} {stars}")
print(f"\nR²: {model2.rsquared:.3f} | Adj. R²: {model2.rsquared_adj:.3f}")

# MODEL 3: Add PM2.5 (2001-2020 only)

m3_data = df[
    (df['Year'] >= 2001) & (df['Year'] <= 2020)
][['Country Code', 'life_expectancy', 'log_gdp', 'Year',
   'edu_expenditure_pct_gdp', 'health_exp_pct_gdp', 'pm25']].dropna()

model3 = smf.ols(
    'life_expectancy ~ log_gdp + Year + edu_expenditure_pct_gdp + health_exp_pct_gdp + pm25',
    data=m3_data
).fit(cov_type='HC1')

print("\n" + "=" * 65)
print("MODEL 3: + PM2.5 (subsample 2001-2020)")

print(
    f"Observations: {int(model3.nobs):,} | Countries: {m3_data['Country Code'].nunique()}")
print("=" * 65)
print(f"{'Variable':<30} {'Coef':>8} {'Std Err':>10} {'p-value':>10}")
print("-" * 65)
for var in ['Intercept', 'log_gdp', 'Year', 'edu_expenditure_pct_gdp',
            'health_exp_pct_gdp', 'pm25']:
    coef = model3.params[var]
    se = model3.bse[var]
    pval = model3.pvalues[var]
    stars = '***' if pval < 0.01 else '**' if pval < 0.05 else '*' if pval < 0.1 else ''
    print(f"{var:<30} {coef:>8.3f} {se:>10.3f} {pval:>10.4f} {stars}")
print(f"\nR²: {model3.rsquared:.3f} | Adj. R²: {model3.rsquared_adj:.3f}")

#  VIF Check

print("\n" + "=" * 65)
print("MULTICOLLINEARITY CHECK (VIF) - Model 3 Predictors")
print("=" * 65)
vif_data = m3_data[['log_gdp', 'Year', 'edu_expenditure_pct_gdp',
                    'health_exp_pct_gdp', 'pm25']].dropna()
vif_data = (vif_data - vif_data.mean()) / vif_data.std()
vif_results = pd.DataFrame({
    'Variable': vif_data.columns,
    'VIF': [variance_inflation_factor(vif_data.values, i)
            for i in range(vif_data.shape[1])]
})
print(vif_results.round(2).to_string(index=False))
print("\nNote: VIF > 10 indicates serious multicollinearity")

# Save results
results = {
    'Model': ['Model 1', 'Model 2', 'Model 3'],
    'N_obs': [int(model1.nobs), int(model2.nobs), int(model3.nobs)],
    'R2': [round(model1.rsquared, 3), round(model2.rsquared, 3), round(model3.rsquared, 3)],
    'Adj_R2': [round(model1.rsquared_adj, 3), round(model2.rsquared_adj, 3), round(model3.rsquared_adj, 3)]
}
pd.DataFrame(results).to_csv('regression_summary.csv', index=False)
print("\n Regression analysis complete. Results saved.")
