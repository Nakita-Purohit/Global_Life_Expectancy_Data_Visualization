import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor


# Robustness Checks
# Inputs: master_panel.csv (created by your merge/clean script)
# Outputs:
#   - robustness_results.csv
#   - vif_model3.csv


DATA_FILE = "master_panel.csv"


# Helper: running OLS with HC1 SE


def run_ols(df_in, y_col, x_cols):
    X = df_in[x_cols].copy()
    X = sm.add_constant(X)
    y = df_in[y_col]
    model = sm.OLS(y, X).fit(cov_type="HC1")
    return model


def safe_get(model, name):
    """Return (coef, pvalue) if exists else (None, None)."""
    if name in model.params.index:
        return float(model.params[name]), float(model.pvalues[name])
    return None, None


# Loads data
df = pd.read_csv(DATA_FILE)

# Basic sanity filters (optional but safe)
df = df[df["Year"].between(2000, 2023)]
df = df[df["Country Code"].astype(str).str.len() == 3]  # ISO3 only


# CHECK 1: Pre-2020 re-runs (Model 1 and Model 2)


df_pre = df[df["Year"] <= 2019].copy()

# Model 1 pre-2020
m1_pre = df_pre[["Country Code",
                 "life_expectancy", "log_gdp", "Year"]].dropna()
r1 = run_ols(m1_pre, "life_expectancy", ["log_gdp", "Year"])

# Model 2 pre-2020
m2_pre = df_pre[[
    "Country Code", "life_expectancy", "log_gdp", "Year",
    "edu_expenditure_pct_gdp", "health_exp_pct_gdp"
]].dropna()
r2 = run_ols(m2_pre, "life_expectancy", [
             "log_gdp", "Year", "edu_expenditure_pct_gdp", "health_exp_pct_gdp"])


# CHECK 2: GDP outlier trimming (Model 1 trimmed 1% tails)


g = df["gdp_per_capita"].dropna()
low, high = g.quantile(0.01), g.quantile(0.99)

df_trim = df[df["gdp_per_capita"].between(low, high)].copy()
m1_trim = df_trim[["Country Code",
                   "life_expectancy", "log_gdp", "Year"]].dropna()
r1t = run_ols(m1_trim, "life_expectancy", ["log_gdp", "Year"])


# CHECK 3: VIF for Model 3 predictors (2001–2020 complete cases)


m3 = df[df["Year"].between(2001, 2020)][[
    "life_expectancy", "log_gdp", "Year",
    "edu_expenditure_pct_gdp", "health_exp_pct_gdp", "pm25"
]].dropna()

X_vif = m3[["log_gdp", "Year", "edu_expenditure_pct_gdp",
            "health_exp_pct_gdp", "pm25"]].copy()
X_vif = sm.add_constant(X_vif)

vif_rows = []
for i, col in enumerate(X_vif.columns):
    if col == "const":
        continue
    vif_rows.append({
        "Variable": col,
        "VIF": round(variance_inflation_factor(X_vif.values, i), 2)
    })

vif_df = pd.DataFrame(vif_rows)
vif_df.to_csv("vif_model3.csv", index=False)


# Saving robustness summary


robust_rows = []

# Pre-2020 Model 1
coef, p = safe_get(r1, "log_gdp")
robust_rows.append({
    "Check": "Pre2020_Model1",
    "N_obs": int(r1.nobs),
    "Countries": int(m1_pre["Country Code"].nunique()),
    "R2": round(r1.rsquared, 3),
    "Adj_R2": round(r1.rsquared_adj, 3),
    "log_gdp_coef": round(coef, 3) if coef is not None else None,
    "log_gdp_p": round(p, 4) if p is not None else None,
    "health_exp_coef": None,
    "health_exp_p": None,
    "edu_exp_coef": None,
    "edu_exp_p": None
})

# Pre-2020 Model 2
coef_g, p_g = safe_get(r2, "log_gdp")
coef_h, p_h = safe_get(r2, "health_exp_pct_gdp")
coef_e, p_e = safe_get(r2, "edu_expenditure_pct_gdp")

robust_rows.append({
    "Check": "Pre2020_Model2",
    "N_obs": int(r2.nobs),
    "Countries": int(m2_pre["Country Code"].nunique()),
    "R2": round(r2.rsquared, 3),
    "Adj_R2": round(r2.rsquared_adj, 3),
    "log_gdp_coef": round(coef_g, 3) if coef_g is not None else None,
    "log_gdp_p": round(p_g, 4) if p_g is not None else None,
    "health_exp_coef": round(coef_h, 3) if coef_h is not None else None,
    "health_exp_p": round(p_h, 4) if p_h is not None else None,
    "edu_exp_coef": round(coef_e, 3) if coef_e is not None else None,
    "edu_exp_p": round(p_e, 4) if p_e is not None else None
})

# Trimmed GDP Model 1
coef_t, p_t = safe_get(r1t, "log_gdp")
robust_rows.append({
    "Check": "TrimmedGDP_Model1_1pct",
    "N_obs": int(r1t.nobs),
    "Countries": int(m1_trim["Country Code"].nunique()),
    "R2": round(r1t.rsquared, 3),
    "Adj_R2": round(r1t.rsquared_adj, 3),
    "log_gdp_coef": round(coef_t, 3) if coef_t is not None else None,
    "log_gdp_p": round(p_t, 4) if p_t is not None else None,
    "health_exp_coef": None,
    "health_exp_p": None,
    "edu_exp_coef": None,
    "edu_exp_p": None
})

robust_df = pd.DataFrame(robust_rows)
robust_df.to_csv("robustness_results.csv", index=False)

# Console output (for logs)

print("\n ROBUSTNESS SUMMARY SAVED")
print(robust_df.to_string(index=False))

print("\n VIF SAVED (Model 3 predictors) ")
print(vif_df.to_string(index=False))

print("\n Robustness checks complete.")
