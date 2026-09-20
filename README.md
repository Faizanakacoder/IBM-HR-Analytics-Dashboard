# 🏢 HR Employee Attrition – BI Dashboard

> Interactive single-page dashboard built with **Plotly Dash** on the IBM HR Analytics dataset to surface workforce attrition drivers and support retention decisions.

---

## 🔍 Overview

| | |
|---|---|
| **Dataset** | IBM HR Analytics · 1,470 employees · 35 features |
| **App** | Single-file Dash app (`app.py`) — frontend + backend combined |
| **Filters** | Department · Gender · Age Range (live, cascades across all charts) |
| **KPIs** | Total Employees · Attrited · Attrition Rate · Avg Income · Avg Tenure · Avg Age |
| **Charts** | 10 interactive Plotly charts + sortable/filterable data table |

---

## 💡 Business Insights

- 🔴 **Overtime** employees leave at ~27.5% vs ~9.4% for non-overtime — nearly **3× higher risk**
- 📊 **Sales Representatives** carry the highest role-level attrition at **33.3%**
- 👶 Employees aged **18–25** have the highest attrition rate of any age band
- 💍 **Single** employees leave significantly more than married or divorced peers
- 💸 Attrited employees earn a **lower median income** (~$4,787 vs $6,833 retained)
- 😞 **Low Job Satisfaction** and **frequent business travel** are strong exit predictors
- 🗓️ The **first 1–3 years** at Job Levels 1–2 is the highest-risk tenure window

---

## 🛠️ Tech Stack

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![Dash](https://img.shields.io/badge/Dash-2.17+-00ADD8?style=flat&logo=plotly&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-5.22+-3F4F75?style=flat&logo=plotly&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.2+-150458?style=flat&logo=pandas&logoColor=white)
![Bootstrap](https://img.shields.io/badge/DBC-Bootstrap%205-7952B3?style=flat&logo=bootstrap&logoColor=white)
![Gunicorn](https://img.shields.io/badge/Gunicorn-21.2+-499848?style=flat&logo=gunicorn&logoColor=white)

---

## 🚀 Quick Start

```bash
# 1. Clone
git clone <repo-url> && cd <project-folder>

# 2. Place dataset (rename if needed)
#    WA_Fn-UseC_-HR-Employee-Attrition.csv  ← must be in same folder as app.py
#    Dataset: https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset

# 3. Install
pip install -r requirements.txt

# 4. Run
python app.py
# → http://127.0.0.1:8050

# Production
gunicorn app:server -b 0.0.0.0:8050
```

---

## 🗂️ Project Structure

```
├── app.py                                   # Full Dash app (frontend + backend)
├── requirements.txt                         # Python dependencies
├── README.md                                # This file
├── HR_Attrition_Project_Report.docx         # Business intelligence report (.docx)
└── WA_Fn-UseC_-HR-Employee-Attrition.csv   # Dataset (not included in repo)
```

---

## 📸 Dashboard Screenshots

### Full Dashboard — KPIs, Filters & Top Charts
![Full HR Employee Attrition Dashboard showing filters, KPI cards, and Attrition by Department and Age Band charts](1_Full%20Dashboard%20%E2%80%94%20KPIs%2C%20Filters%20%26%20Top%20Charts.png)

### Overtime vs Attrition · Attrition Rate by Job Role
![Donut charts comparing overtime vs non-overtime attrition, and horizontal bar chart of attrition rate by job role](2_Overtime%20vs%20Attrition%20%C2%B7%20Attrition%20Rate%20by%20Job%20Role.png)

### Monthly Income Distribution · Job Satisfaction vs Attrition
![Box plot of monthly income split by attrition status, and grouped bar chart of job satisfaction levels vs attrition](3_Monthly%20Income%20Distribution%20%C2%B7%20Job%20Satisfaction%20vs%20Attrition.png)

### Attrition by Marital Status · Business Travel · Work-Life Balance
![Three grouped bar charts showing attrition by marital status, business travel frequency, and work-life balance rating](4_Attrition%20by%20Marital%20Status%20%C2%B7%20Business%20Travel%20%C2%B7%20Work-Life%20Balance.png)

### Attrition Heatmap — Years at Company × Job Level
![Heatmap showing attrition concentration at Job Level 1 and 0–5 years tenure](5_Attrition%20Heatmap%20%E2%80%94%20Years%20at%20Company%20%C3%97%20Job%20Level.png)

### Employee Detail Table
![Paginated sortable filterable employee detail table with attrited rows highlighted in red](6_Employee%20Detail%20Table.png)

### Dash Callback Graph
![Dash callback dependency graph showing 3 filter inputs driving 12 outputs across all charts and KPIs](7_Dash%20Callback%20Graph.png)

---

## 📄 License

This project is licensed under the [MIT License](LICENSE). 

Dataset © IBM via Kaggle.
