import pandas as pd
import numpy as np

# =========================
# 1. LOAD DATASETS
# =========================
rain = pd.read_csv("rainfall_data.csv")
river = pd.read_csv("river_data.csv")
ground = pd.read_csv("groundwater_data.csv")

print("Rain shape:", rain.shape)
print("River shape:", river.shape)
print("Groundwater shape:", ground.shape)

# =========================
# 2. CLEAN COLUMN NAMES
# =========================
rain.columns = rain.columns.str.strip()
river.columns = river.columns.str.strip()
ground.columns = ground.columns.str.strip()

# Rename columns
rain = rain.rename(columns={"Hourly Rainfall": "rainfall"})
river = river.rename(columns={"Hourly Water Level": "river_water_level"})
ground = ground.rename(columns={"Ground Water Level": "groundwater_level"})

# =========================
# 3. STANDARDIZE DISTRICT NAMES
# =========================
for df in [rain, river, ground]:
    df["District"] = df["District"].astype(str).str.strip().str.title()

# =========================
# 4. PARSE DATETIME
# =========================
for df in [rain, river, ground]:
    df["Data Acquisition Time"] = pd.to_datetime(df["Data Acquisition Time"], errors="coerce")

# =========================
# 5. CONVERT NUMERIC COLUMNS
# =========================
rain["rainfall"] = pd.to_numeric(rain["rainfall"], errors="coerce")
river["river_water_level"] = pd.to_numeric(river["river_water_level"], errors="coerce")
ground["groundwater_level"] = pd.to_numeric(ground["groundwater_level"], errors="coerce")

# =========================
# 6. MAKE DISTRICT CODE SAME TYPE
# =========================
for df in [rain, river, ground]:
    df["District LGD Code"] = pd.to_numeric(df["District LGD Code"], errors="coerce")

# =========================
# 7. DROP INVALID ROWS
# =========================
rain = rain.dropna(subset=["Data Acquisition Time", "District LGD Code", "District"])
river = river.dropna(subset=["Data Acquisition Time", "District LGD Code", "District"])
ground = ground.dropna(subset=["Data Acquisition Time", "District LGD Code", "District"])

# Convert district code to int after dropping NaNs
for df in [rain, river, ground]:
    df["District LGD Code"] = df["District LGD Code"].astype(int)

# =========================
# 8. REMOVE DUPLICATES
# =========================
rain = rain.drop_duplicates()
river = river.drop_duplicates()
ground = ground.drop_duplicates()

# =========================
# 9. KEEP ONLY NEEDED COLUMNS
# =========================
rain = rain[["Data Acquisition Time", "District LGD Code", "District", "rainfall"]]
river = river[["Data Acquisition Time", "District LGD Code", "District", "river_water_level"]]
ground = ground[["Data Acquisition Time", "District LGD Code", "District", "groundwater_level"]]

# =========================
# 10. SORT EXACTLY FOR MERGE_ASOF
# IMPORTANT: sort by time first, then by district code
# =========================
rain = rain.sort_values(["Data Acquisition Time", "District LGD Code"]).reset_index(drop=True)
river = river.sort_values(["Data Acquisition Time", "District LGD Code"]).reset_index(drop=True)
ground = ground.sort_values(["Data Acquisition Time", "District LGD Code"]).reset_index(drop=True)

# =========================
# 11. MERGE RIVER INTO RAINFALL
# =========================
merged = pd.merge_asof(
    rain,
    river[["Data Acquisition Time", "District LGD Code", "river_water_level"]],
    on="Data Acquisition Time",
    by="District LGD Code",
    direction="nearest",
    tolerance=pd.Timedelta("6h")
)

# =========================
# 12. MERGE GROUNDWATER INTO RESULT
# =========================
merged = pd.merge_asof(
    merged,
    ground[["Data Acquisition Time", "District LGD Code", "groundwater_level"]],
    on="Data Acquisition Time",
    by="District LGD Code",
    direction="nearest",
    tolerance=pd.Timedelta("7D")
)

# =========================
# 13. FINAL CLEANUP
# =========================
merged = merged.drop_duplicates()

final_cols = [
    "Data Acquisition Time",
    "District LGD Code",
    "District",
    "rainfall",
    "river_water_level",
    "groundwater_level"
]

merged = merged[final_cols]

# =========================
# 14. SAVE OUTPUT
# =========================
merged.to_csv("merged_raw_dataset.csv", index=False)

print("\nMerged dataset saved as: merged_raw_dataset.csv")
print("Merged shape:", merged.shape)

print("\nFirst 5 rows:")
print(merged.head())

print("\nMissing values:")
print(merged.isnull().sum())

print("\nDuplicate rows in merged:", merged.duplicated().sum())