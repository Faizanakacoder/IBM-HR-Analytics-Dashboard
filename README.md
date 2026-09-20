# HR Employee Attrition – Business Intelligence Dashboard

An interactive, single-page BI dashboard built with **Plotly Dash** and **Dash Bootstrap Components**,
powered by the IBM HR Analytics Employee Attrition dataset.

---

## 📊 Features

| Section | Details |
|---|---|
| **KPI Strip** | Total Employees · Attrited · Attrition Rate · Avg Monthly Income · Avg Tenure · Avg Age |
| **Filters** | Department · Gender · Age Range (slider) |
| **Charts** | 10 interactive charts covering attrition by dept, age band, job role, overtime, income, job satisfaction, marital status, travel, work-life balance, and a heatmap |
| **Data Table** | Filterable + sortable employee detail table |

---

## 🚀 Quick Start

### 1. Clone / Download
```bash
git clone <repo-url>
cd <project-folder>
```

### 2. Place the Dataset
Download the dataset from the link below and place the CSV file in the **same directory** as `app.py`:

> 📁 **Dataset:** [IBM HR Analytics Employee Attrition & Performance — Kaggle](<PASTE_DATASET_LINK_HERE>)

The file must be named exactly:
```
WA_Fn-UseC_-HR-Employee-Attrition.csv
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the App
```bash
python app.py
```

Open your browser at **http://127.0.0.1:8050**

---

## 🗂 Project Structure

```
├── app.py                                    # Full Dash app (frontend + backend)
├── requirements.txt                          # Python dependencies
├── README.md                                 # This file
├── HR_Attrition_Project_Report.docx          # Business intelligence report
└── WA_Fn-UseC_-HR-Employee-Attrition.csv    # Dataset (not included in repo)
```

---

## 📦 Dependencies

| Package | Purpose |
|---|---|
| `dash` | Core web framework |
| `dash-bootstrap-components` | Bootstrap-themed layout components |
| `plotly` | Interactive chart engine |
| `pandas` | Data loading & transformation |
| `gunicorn` | Production WSGI server (optional) |

---

## 🌐 Deploying to Production

```bash
gunicorn app:server -b 0.0.0.0:8050
```

---

## 🔑 Key Business Insights (Preview)

- Employees who work **overtime** have a significantly higher attrition rate (~30% vs ~10%).
- The **Sales** department and **Sales Representative** role exhibit the highest attrition rates.
- Employees aged **18–25** leave at the highest rate compared to all other age groups.
- **Single** employees are more likely to leave than married or divorced counterparts.
- Low **Job Satisfaction** and low **Work-Life Balance** are strongly correlated with attrition.
- Lower **Monthly Income** employees are disproportionately represented in attrition cases.

---

## 📄 License

This project is for educational and internship purposes.  
Dataset source: IBM (via Kaggle). All rights reserved to the original authors.
