import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

# =========================
# 1. LOAD DATA
# =========================
flood_df = pd.read_csv("flood_risk_dataset.csv")
flood_df["Data Acquisition Time"] = pd.to_datetime(flood_df["Data Acquisition Time"], errors="coerce")

# Sort properly
flood_df = flood_df.sort_values(["District", "Data Acquisition Time"]).reset_index(drop=True)

# =========================
# 2. DATETIME FEATURES
# =========================
flood_df["year"] = flood_df["Data Acquisition Time"].dt.year
flood_df["month"] = flood_df["Data Acquisition Time"].dt.month
flood_df["day"] = flood_df["Data Acquisition Time"].dt.day
flood_df["hour"] = flood_df["Data Acquisition Time"].dt.hour
flood_df["day_of_week"] = flood_df["Data Acquisition Time"].dt.dayofweek

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

flood_df["season"] = flood_df["month"].apply(get_season)

# =========================
# 3. LAG FEATURES (district-wise)
# =========================
flood_df["rainfall_lag_1"] = flood_df.groupby("District")["rainfall"].shift(1)
flood_df["rainfall_lag_3"] = flood_df.groupby("District")["rainfall"].shift(3)

flood_df["river_lag_1"] = flood_df.groupby("District")["river_water_level"].shift(1)
flood_df["river_lag_3"] = flood_df.groupby("District")["river_water_level"].shift(3)

flood_df["groundwater_lag_1"] = flood_df.groupby("District")["groundwater_level"].shift(1)
flood_df["groundwater_lag_3"] = flood_df.groupby("District")["groundwater_level"].shift(3)

# =========================
# 4. ROLLING FEATURES
# =========================
flood_df["rainfall_roll_3"] = flood_df.groupby("District")["rainfall"].transform(lambda x: x.rolling(3).mean())
flood_df["rainfall_roll_6"] = flood_df.groupby("District")["rainfall"].transform(lambda x: x.rolling(6).mean())

flood_df["river_roll_3"] = flood_df.groupby("District")["river_water_level"].transform(lambda x: x.rolling(3).mean())
flood_df["river_roll_6"] = flood_df.groupby("District")["river_water_level"].transform(lambda x: x.rolling(6).mean())

flood_df["groundwater_roll_3"] = flood_df.groupby("District")["groundwater_level"].transform(lambda x: x.rolling(3).mean())
flood_df["groundwater_roll_6"] = flood_df.groupby("District")["groundwater_level"].transform(lambda x: x.rolling(6).mean())

# =========================
# 5. DIFFERENCE FEATURES
# =========================
flood_df["rainfall_diff_1"] = flood_df.groupby("District")["rainfall"].diff(1)
flood_df["river_diff_1"] = flood_df.groupby("District")["river_water_level"].diff(1)
flood_df["groundwater_diff_1"] = flood_df.groupby("District")["groundwater_level"].diff(1)

# =========================
# 6. DROP NaNs CREATED BY LAGS
# =========================
flood_df = flood_df.dropna().reset_index(drop=True)

# =========================
# 7. CREATE FLOOD RISK SCORE
# =========================
scaler = MinMaxScaler()

score_features = flood_df[["rainfall", "river_water_level", "groundwater_level"]].copy()
scaled = scaler.fit_transform(score_features)

scaled_df = pd.DataFrame(scaled, columns=["rainfall_scaled", "river_scaled", "ground_scaled"])

# Weighted flood risk score
# You can tune weights later if needed
flood_df["flood_risk_score"] = (
    0.4 * scaled_df["rainfall_scaled"] +
    0.4 * scaled_df["river_scaled"] +
    0.2 * scaled_df["ground_scaled"]
)

# =========================
# 8. CREATE FLOOD RISK CATEGORY
# =========================
low_thresh = flood_df["flood_risk_score"].quantile(0.33)
high_thresh = flood_df["flood_risk_score"].quantile(0.66)

def categorize_risk(score):
    if score <= low_thresh:
        return "Low"
    elif score <= high_thresh:
        return "Medium"
    else:
        return "High"

flood_df["flood_risk_category"] = flood_df["flood_risk_score"].apply(categorize_risk)

# =========================
# 9. SAVE FINAL MODEL DATASET
# =========================
flood_df.to_csv("flood_model_dataset.csv", index=False)

print("Flood model dataset saved as: flood_model_dataset.csv")
print("Shape:", flood_df.shape)

print("\nColumns:")
print(flood_df.columns.tolist())

print("\nFirst 5 rows:")
print(flood_df.head())

print("\nRisk Category Distribution:")
print(flood_df["flood_risk_category"].value_counts())

print("\nMissing values:")
print(flood_df.isnull().sum())