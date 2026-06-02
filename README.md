# 🚔 AI Crime Hotspot Prediction & Police Patrol Optimization System

## Overview

AI Crime Hotspot Prediction & Police Patrol Optimization System is a Machine Learning-based web application designed to predict crime risk levels, identify dangerous districts, generate police intelligence reports, and support crime analysis through interactive dashboards.

The system helps law enforcement agencies make data-driven decisions by analyzing historical crime records and forecasting future crime trends.

---

## Features

### Crime Prediction

* Predict future crime count using Machine Learning
* State-wise and district-wise crime analysis
* Risk level classification (High, Medium, Low)

### AI Recommendations

* Automated police action recommendations
* Patrol optimization suggestions
* Crime prevention insights

### Smart Crime Alert System

* High-risk area alerts
* Medium-risk area notifications
* Low-risk area monitoring suggestions

### Crime Category Prediction

* Identifies dominant crime categories
* Displays district-level crime patterns

### Interactive Dashboard

* Crime statistics dashboard
* Top dangerous states visualization
* Crime trend forecasting
* District ranking system

### Crime Heatmap

* Interactive hotspot visualization using Folium Maps
* Crime-prone city identification

### Police Intelligence Report

* Downloadable PDF reports
* Risk assessment summary
* AI-generated recommendations

### Multi CSV Upload & Auto Analysis

* Upload multiple crime datasets
* Automatic crime analysis
* Trend visualization
* State-wise crime comparison

### Secure Login System

* Admin access
* Police Officer access
* Role-based functionality

---

## Technology Stack

### Programming Language

* Python

### Machine Learning

* Scikit-Learn
* Random Forest Regressor

### Data Analysis

* Pandas
* NumPy

### Visualization

* Matplotlib
* Folium

### Web Application

* Streamlit

### Report Generation

* ReportLab

---

## Dataset Requirements

The system supports crime datasets containing:

Required Columns:

```text
STATE/UT
DISTRICT
YEAR
```

Recommended Column:

```text
TOTAL IPC CRIMES
```

If TOTAL IPC CRIMES is not available, the system automatically calculates crime totals using available numeric crime columns.

---

## Machine Learning Workflow

1. Load crime dataset
2. Data cleaning and preprocessing
3. Encode state and district values
4. Train Random Forest Regressor
5. Save trained model and encoders
6. Predict future crime count
7. Classify risk level
8. Generate recommendations
9. Create police intelligence report

---

## Risk Levels

### 🔴 High Risk

* Increase police patrol frequency
* Deploy additional officers
* Activate CCTV monitoring
* Strengthen night surveillance

### 🟠 Medium Risk

* Regular patrol required
* Monitor suspicious activities
* Improve emergency response

### 🟢 Low Risk

* Maintain routine monitoring
* Continue community policing
* Keep surveillance systems active

---

## Project Structure

```text
AI-Crime-Hotspot-Prediction
│
├── app.py
├── crime.csv
├── requirements.txt
├── README.md
│
├── models
│   ├── crime_model.pkl
│   ├── state_encoder.pkl
│   └── district_encoder.pkl
│
└── src
    ├── train_model.py
    └── data_cleaning.py
```

---

## Installation

Install dependencies:

```bash
pip install -r requirements.txt
```

Run application:

```bash
streamlit run app.py
```

---

## Login Credentials

### Admin

```text
Password: crime@admin
```

### Police Officer

```text
Password: police@secure
```

---

## Outputs

The application provides:

* Crime prediction
* Risk classification
* AI recommendations
* Crime category analysis
* District rankings
* Crime heatmap
* Trend forecasting
* PDF intelligence reports
* Multi CSV analytics

---

## Future Enhancements

* Real-time crime data integration
* Database connectivity
* Advanced forecasting models
* Police station-level analytics
* Mobile application support
* Automated model retraining

---

## Author

Praveen M

Bachelor of Engineering (Computer Science and Engineering)

Python | Machine Learning | Data Analytics | Streamlit


