import pandas as pd

# Load original files again
rain = pd.read_csv("rainfall_data.csv")
river = pd.read_csv("river_data.csv")
ground = pd.read_csv("groundwater_data.csv")

# Clean columns
rain.columns = rain.columns.str.strip()
river.columns = river.columns.str.strip()
ground.columns = ground.columns.str.strip()

# Standardize district names
for df in [rain, river, ground]:
    df["District"] = df["District"].astype(str).str.strip().str.title()

# Parse datetime
for df in [rain, river, ground]:
    df["Data Acquisition Time"] = pd.to_datetime(df["Data Acquisition Time"], errors="coerce")

# -----------------------------
# BASIC SHAPES
# -----------------------------
print("Rain shape:", rain.shape)
print("River shape:", river.shape)
print("Ground shape:", ground.shape)

# -----------------------------
# UNIQUE DISTRICTS
# -----------------------------
print("\nUnique districts in Rain:", rain["District"].nunique())
print("Unique districts in River:", river["District"].nunique())
print("Unique districts in Ground:", ground["District"].nunique())

print("\nDistricts in Rain:")
print(sorted(rain["District"].dropna().unique()))

print("\nDistricts in River:")
print(sorted(river["District"].dropna().unique()))

print("\nDistricts in Ground:")
print(sorted(ground["District"].dropna().unique()))

# -----------------------------
# COMMON DISTRICTS
# -----------------------------
rain_d = set(rain["District"].dropna().unique())
river_d = set(river["District"].dropna().unique())
ground_d = set(ground["District"].dropna().unique())

common_all = rain_d & river_d & ground_d
print("\nCommon districts in ALL 3 datasets:", len(common_all))
print(sorted(common_all))

# -----------------------------
# DATE RANGES
# -----------------------------
print("\nRain date range:", rain["Data Acquisition Time"].min(), "to", rain["Data Acquisition Time"].max())
print("River date range:", river["Data Acquisition Time"].min(), "to", river["Data Acquisition Time"].max())
print("Ground date range:", ground["Data Acquisition Time"].min(), "to", ground["Data Acquisition Time"].max())

# -----------------------------
# ROW COUNTS PER DISTRICT
# -----------------------------
print("\nRain rows per district:")
print(rain["District"].value_counts())

print("\nRiver rows per district:")
print(river["District"].value_counts())

print("\nGround rows per district:")
print(ground["District"].value_counts())