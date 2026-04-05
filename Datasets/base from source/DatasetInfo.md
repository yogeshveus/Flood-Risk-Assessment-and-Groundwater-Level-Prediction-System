# Dataset Information

## 1. Overview

This project utilizes a combination of **hydrological, meteorological, and geospatial datasets** to develop a predictive analytics system for **groundwater level forecasting** and **flood risk assessment** in Tamil Nadu, India. The datasets are collected from multiple authoritative sources and integrated into a unified framework for analysis and modeling.

---

## 2. Dataset Sources and Description

### 2.1 Rainfall Data

**Links:**
- https://data.opencity.in/dataset/chennai-rainfall-data/resource/fd176db8-caca-42e5-b5a0-9dc78a3d73a9  
- https://nwdp.nwic.gov.in/dataset/rainfall-telemetry-hourly-tamil-nadu-sw-gw  
- https://nwdp.nwic.gov.in/dataset/rainfall-manual-hourly-tamil-nadu-sw-gw-department  

**Description:**  
Contains historical rainfall measurements recorded at hourly and daily intervals across multiple stations in Tamil Nadu.

**Usage in Project:**
- Primary input variable for both groundwater prediction and flood risk classification
- Used to generate lag features and cumulative rainfall indicators

---

### 2.2 River Water Level and Discharge Data

**Links:**
- https://nwdp.nwic.gov.in/dataset/river-water-level-telemetry-hourly-tamil-nadu-sw-and-gw-department  
- https://nwdp.nwic.gov.in/dataset/river-discharge-manual-dailly-tamil-nadu-surface-water-groundwater-department  

**Description:**  
Provides information on river water levels and discharge rates at various monitoring stations.

**Usage in Project:**
- Used for flood risk classification
- Helps define flood thresholds (Low, Medium, High)

---

### 2.3 Groundwater Level Data

**Links:**
- https://nwdp.nwic.gov.in/dataset/gwl-manual-quarterly-central-ground-water-board-department  
- https://nwdp.nwic.gov.in/dataset/ground-water-level-telemetry-daily-tamil-nadu-sw-gw  

**Description:**  
Contains groundwater level measurements collected at regular intervals across observation wells.

**Usage in Project:**
- Target variable for regression models
- Used for time-series forecasting

---

### 2.4 Digital Elevation Model (DEM)

**Link:**
- https://swat.tamu.edu/data/india-dataset/

**Description:**  
Provides elevation data representing terrain characteristics such as height, slope, and drainage patterns.

**Usage in Project:**
- Extraction of terrain features (slope, flow accumulation)
- Helps identify flood-prone regions

---

### 2.5 Land Use / Land Cover (LULC)

**Link:**
- https://swat.tamu.edu/data/india-dataset/

**Description:**  
Classifies land into categories such as urban, agricultural, forest, and water bodies.

**Usage in Project:**
- Used to estimate runoff characteristics
- Helps differentiate urban and rural flood behavior

---

### 2.6 Soil Data

**Source:** SWAT India Dataset (HWSD/FAO)

**Link:**
- https://swat.tamu.edu/data/india-dataset/

**Description:**  
Provides soil characteristics including texture, depth, and water retention capacity.

**Usage in Project:**
- Used for groundwater recharge modeling
- Influences infiltration and runoff behavior
