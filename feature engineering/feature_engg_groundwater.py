import pandas as pd
import numpy as np

# =========================
# 1. LOAD DATA
# =========================
gw_df = pd.read_csv("groundwater_prediction_dataset.csv")
gw_df["Data Acquisition Time"] = pd.to_datetime(gw_df["Data Acquisition Time"], errors="coerce")

# Sort properly
gw_df = gw_df.sort_values(["District", "Data Acquisition Time"]).reset_index(drop=True)

# =========================
# 2. DATETIME FEATURES
# =========================
gw_df["year"] = gw_df["Data Acquisition Time"].dt.year
gw_df["month"] = gw_df["Data Acquisition Time"].dt.month
gw_df["day"] = gw_df["Data Acquisition Time"].dt.day
gw_df["hour"] = gw_df["Data Acquisition Time"].dt.hour
gw_df["day_of_week"] = gw_df["Data Acquisition Time"].dt.dayofweek

# Season mapping
def get_season(month):
    if month in [12, 1, 2]:
        return "Winter"
    elif month in [3, 4, 5]:
        return "Summer"
    elif month in [6, 7, 8, 9]:
        return "Monsoon"
    else:
        return "Post-Monsoon"

gw_df["season"] = gw_df["month"].apply(get_season)

# =========================
# 3. LAG FEATURES (district-wise)
# =========================
gw_df["rainfall_lag_1"] = gw_df.groupby("District")["rainfall"].shift(1)
gw_df["rainfall_lag_3"] = gw_df.groupby("District")["rainfall"].shift(3)
gw_df["rainfall_lag_6"] = gw_df.groupby("District")["rainfall"].shift(6)

gw_df["groundwater_lag_1"] = gw_df.groupby("District")["groundwater_level"].shift(1)
gw_df["groundwater_lag_3"] = gw_df.groupby("District")["groundwater_level"].shift(3)
gw_df["groundwater_lag_6"] = gw_df.groupby("District")["groundwater_level"].shift(6)

# =========================
# 4. ROLLING FEATURES (district-wise)
# =========================
gw_df["rainfall_roll_3"] = gw_df.groupby("District")["rainfall"].transform(lambda x: x.rolling(window=3).mean())
gw_df["rainfall_roll_6"] = gw_df.groupby("District")["rainfall"].transform(lambda x: x.rolling(window=6).mean())

gw_df["groundwater_roll_3"] = gw_df.groupby("District")["groundwater_level"].transform(lambda x: x.rolling(window=3).mean())
gw_df["groundwater_roll_6"] = gw_df.groupby("District")["groundwater_level"].transform(lambda x: x.rolling(window=6).mean())

# =========================
# 5. OPTIONAL: CHANGE FEATURES
# =========================
gw_df["rainfall_diff_1"] = gw_df.groupby("District")["rainfall"].diff(1)
gw_df["groundwater_diff_1"] = gw_df.groupby("District")["groundwater_level"].diff(1)

# =========================
# 6. DROP ROWS WITH NaNs CREATED BY LAGS
# =========================
gw_df = gw_df.dropna().reset_index(drop=True)

# =========================
# 7. SAVE FINAL MODEL DATASET
# =========================
gw_df.to_csv("groundwater_model_dataset.csv", index=False)

print("Groundwater model dataset saved as: groundwater_model_dataset.csv")
print("Shape:", gw_df.shape)

print("\nColumns:")
print(gw_df.columns.tolist())

print("\nFirst 5 rows:")
print(gw_df.head())

print("\nMissing values:")
print(gw_df.isnull().sum())