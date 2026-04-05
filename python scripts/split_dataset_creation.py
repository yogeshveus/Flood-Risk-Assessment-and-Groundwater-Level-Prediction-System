import pandas as pd

# =========================
# 1. LOAD MERGED DATASET
# =========================
df = pd.read_csv("merged_raw_dataset.csv")

# Parse datetime
df["Data Acquisition Time"] = pd.to_datetime(df["Data Acquisition Time"], errors="coerce")

# Standardize district names
df["District"] = df["District"].astype(str).str.strip().str.title()

print("Original merged shape:", df.shape)
print("\nMissing values:")
print(df.isnull().sum())

# =========================
# 2. DATASET A: GROUNDWATER PREDICTION
# Keep rows where groundwater is available
# =========================
gw_df = df.dropna(subset=["groundwater_level"]).copy()

# Optional: keep rainfall only + groundwater
gw_df = gw_df[[
    "Data Acquisition Time",
    "District LGD Code",
    "District",
    "rainfall",
    "groundwater_level"
]]

gw_df = gw_df.drop_duplicates()
gw_df = gw_df.sort_values(["District", "Data Acquisition Time"]).reset_index(drop=True)

gw_df.to_csv("groundwater_prediction_dataset.csv", index=False)

print("\nGroundwater Prediction Dataset Saved: groundwater_prediction_dataset.csv")
print("Shape:", gw_df.shape)
print("Districts:", gw_df["District"].nunique())
print("Missing values:\n", gw_df.isnull().sum())

# =========================
# 3. DATASET B: FLOOD RISK DATASET
# Keep rows where BOTH river and groundwater exist
# =========================
flood_df = df.dropna(subset=["river_water_level", "groundwater_level"]).copy()

flood_df = flood_df[[
    "Data Acquisition Time",
    "District LGD Code",
    "District",
    "rainfall",
    "river_water_level",
    "groundwater_level"
]]

flood_df = flood_df.drop_duplicates()
flood_df = flood_df.sort_values(["District", "Data Acquisition Time"]).reset_index(drop=True)

flood_df.to_csv("flood_risk_dataset.csv", index=False)

print("\nFlood Risk Dataset Saved: flood_risk_dataset.csv")
print("Shape:", flood_df.shape)
print("Districts:", flood_df["District"].nunique())
print("District names:", sorted(flood_df["District"].unique()))
print("Missing values:\n", flood_df.isnull().sum())