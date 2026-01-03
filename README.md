# 📦 Post-Harvest Loss Analysis (India)

## 📌 Overview

India experiences significant **post-harvest losses**, especially in perishable agricultural produce.  
This repository contains a **data analysis and visualization project** based on publicly available **government datasets**, focusing on **average post-harvest loss percentages** across major crop categories.

The goal of this project is to:
- Analyze crop-wise loss patterns
- Compare losses across multiple years
- Visualize trends and changes
- Provide data-backed context for the need for improved storage infrastructure (e.g., cold storage)

This project is **exploratory and analytical**, not predictive.

---

## 📊 Datasets Used

Two government-reported datasets were used:

### 1️⃣ Dataset: 2019–20
**Columns:**
- `Crops`
- `Commodities`
- `% Avg Loss`

This dataset provides **commodity-level loss percentages**, which were later aggregated at the crop level.

---

### 2️⃣ Dataset: 2021–22
**Columns:**
- `Crops`
- `% Avg Loss`

This dataset is already summarized at the crop level.

---

## 🧹 Data Processing & Cleaning

### 2019–20 Dataset
- Commodities were grouped under their respective crop categories.
- The **mean loss percentage** was calculated for each crop category.
- This produced a summarized dataframe:
  - `Crops`
  - `% Avg Loss`

### 2021–22 Dataset
- Used directly without further aggregation.

### Final Dataset
Both datasets were merged into a single comparison table:

| Crops | 2020 Loss (%) | 2022 Loss (%) | Change (%) |
|------|----------------|----------------|------------|
| Cereals | ... | ... | ... |
| Pulses | ... | ... | ... |
| Fruits | ... | ... | ... |

---

## 📈 Visualizations

The project includes **both static and interactive visualizations**, built using:

- **Matplotlib** – static comparison plots  
- **Seaborn** – styled statistical plots  
- **Plotly** – interactive charts  
- **Dash** – script-based interactive dashboard  

### Key Visuals
- Crop-wise loss comparison (2020 vs 2022)
- Change in loss percentage across years
- Trend lines per crop category
- Loss distribution (pie/donut charts)
- Interactive dashboard for exploration

---

## 🖥 Dashboard

A **script-based Dash dashboard** is included for interactive exploration of the data.

### Dashboard Features
- Year-wise filtering
- Crop-wise comparison
- Trend visualization across years
- Heatmap for quick pattern recognition

This dashboard is intended for:
- Internal analysis
- Demonstration purposes
- Presentation support

---

## ⚠️ Limitations

- The datasets provide **percentage loss**, not absolute quantities (e.g., tons).
- Only two time periods are available.
- Losses are not disaggregated by cause (storage, transport, handling, etc.).

Despite these limitations, percentage-based analysis is sufficient to:
- Identify vulnerable crop categories
- Observe relative trends
- Support infrastructure-related discussions.

---

## 🛠 Technologies Used

- Python  
- Pandas  
- Matplotlib  
- Seaborn  
- Plotly  
- Dash  

---

## 📌 Purpose of This Project

This repository serves as:
- A **data analysis case study**
- A **supporting analysis** for discussions around cold storage and post-harvest infrastructure
- A foundation for future work combining loss data with production volumes, geography, or energy systems

---

## 📜 License

This project is intended for **educational and research purposes**.  
Original data sources belong to their respective government publishers.

