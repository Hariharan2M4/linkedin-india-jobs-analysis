
# 💼 LinkedIn India Jobs — Data Analysis & Job Recommender

An end-to-end data analytics project built on real LinkedIn India job postings,
covering data cleaning, exploratory analysis, and an interactive job recommender app.

## 📁 Project Structure

| File | Description |
|------|-------------|
| `step1_cleaning.py` | Raw data cleaning — deduplication, normalization, feature engineering |
| `linkedin_eda_colab.py` | EDA with 8 visualizations (run in Google Colab) |
| `app.py` | Streamlit job recommender app |
| `linkedin_cleaned.csv` | Cleaned dataset (653 records) |

## 🔍 Key Findings

- **Bengaluru** dominates with 27% of all India data job postings
- **Mid-Senior** is the most in-demand level (40.7%)
- **IT Services & Consulting** is the top hiring industry (17.9%)
- **93% of roles** are Full-time — contract data work is rare in India
- **Data Scientist** outnumbers Data Analyst postings

## 🛠️ Tech Stack

Python · Pandas · Matplotlib · Seaborn · Streamlit

## 🚀 Run the App

pip install streamlit pandas
streamlit run app.py

## 📊 EDA Notebook

Open `linkedin_eda_colab.py` in Google Colab and upload `linkedin_cleaned.csv` when prompted.
