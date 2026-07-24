# 📊 Event Ticket Demand Analysis System

**AI-Powered Demand Prediction for Sports Events**
*IBM Data Science Internship — End-to-End Machine Learning Project*

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)

---

## 🎯 Overview

An enterprise-grade dashboard that predicts event ticket demand using Machine Learning and Explainable AI. The system analyzes 1,385+ sporting events across NBA, NFL, MLB, NHL, and Stadium Tours, leveraging 15+ engineered features to deliver real-time demand predictions with confidence scores and actionable business recommendations.

### Key Features

| Feature | Description |
|---------|-------------|
| **📊 Analytics Dashboard** | 20+ interactive Plotly charts across 5 analysis categories |
| **🎯 Demand Predictor** | Smart auto-fill system — enter 7 inputs, AI retrieves 20+ features |
| **⚖️ Event Comparison** | Side-by-side demand comparison with radar charts |
| **🔬 What-If Analysis** | Scenario simulation (flip weekend, change venue, etc.) |
| **🧠 Explainable AI** | Per-feature contribution analysis with business-readable explanations |
| **📥 Export** | Download prediction reports as TXT or CSV |

---

## 🛠️ Technology Stack

- **Data Processing**: Pandas, NumPy
- **Machine Learning**: Scikit-Learn (Random Forest Regressor, 100 trees)
- **Visualization**: Plotly (20+ chart types)
- **Web Framework**: Streamlit with Custom CSS Design System
- **Serialization**: Joblib

---

## 📁 Project Structure

```
streamlit_app/
├── app.py                          # Main application (6 pages)
├── requirements.txt                # Python dependencies
├── runtime.txt                     # Python version for Streamlit Cloud
├── train_and_save_model.py         # Model training pipeline
├── .gitignore
├── .streamlit/
│   └── config.toml                 # Dark theme configuration
├── output/
│   ├── master_combined_dataset.csv # 1,385 events × 49 columns
│   ├── trained_model.pkl           # Random Forest model (~6.7 MB)
│   ├── preprocessor.pkl            # Feature metadata & importances
│   └── demand_scaler.pkl           # MinMaxScaler for demand scores
├── utils/
│   ├── __init__.py
│   ├── helper.py                   # UI components & CSS design system
│   ├── preprocessing.py            # Smart auto-fill & feature engineering
│   ├── prediction.py               # Prediction engine & Explainable AI
│   ├── visualization.py            # 20+ Plotly chart functions
│   └── recommendation.py           # Similarity engine & report generation
└── assets/
    └── .gitkeep
```

---

## 🚀 Local Setup

### Prerequisites
- Python 3.11+

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/event-demand-analysis.git
cd event-demand-analysis

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## 🚀 Deployment

The application is deployed on **Streamlit Community Cloud** and can be accessed here:

**Live Demo:**  
https://event-ticket-demand-analysis-system-4577.streamlit.app/

## 🧠 How It Works

1. **Data Integration** — Events, Performers, and Venues data merged into a unified dataset
2. **Feature Engineering** — 15+ features including temporal dynamics and star power metrics
3. **Demand Score Formula** — Weighted log-popularity with playoff/weekend multipliers, scaled 0-100
4. **Random Forest Model** — 100 decision trees with top 30 features selected by importance
5. **Smart Prediction** — Enter 7 natural inputs → system auto-fills 20+ features → AI predicts demand
6. **Explainable AI** — Every prediction includes feature contributions and business recommendations

---

## 📊 Dataset

This project utilizes the **public preview** of the **SeatGeek Events & Ticket Listings Dataset** provided by **Rebrowser** for research and educational purposes. The dataset was used for data preprocessing, feature engineering, exploratory data analysis, and machine learning model development.

**Source:**  
https://github.com/rebrowser/seatgeek-dataset

**License:**  
Free for research and non-commercial use with attribution.

**Attribution:**  
© Rebrowser

---

## 🎓 IBM Internship

This project was developed as part of the **IBM Internship Program** under the **Data Analytics and Artificial Intelligence** domain. It demonstrates an end-to-end machine learning workflow, including data preprocessing, feature engineering, exploratory data analysis, model development, evaluation, and deployment through an interactive web application.
