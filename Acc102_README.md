# Project Title: Earnings Quality Analysis & Interactive Tool (Food & Beverage Sector)

**Product Link / Demo:** https://acc102-data-appuct-ryzcejzwsd3xmrmfa8ie6h.streamlit.app/#industry-peer-ranking-accrual-ratio

## 1. Problem & User
This project addresses the challenge of evaluating "earnings quality"—the extent to which reported profits are backed by actual cash—within the food and beverage industry. It is designed for **investors, financial analysts, and accounting students** who need to identify potential financial risks beyond simple revenue growth metrics.

## 2. Data
* **Source:** Custom dataset retrieved from WRDS Compustat Database.
* **Access Date:** April 14, 2026.
* **Key Fields:** Net Income (`ni`), Operating Cash Flow (`oancf`), Total Assets (`at`), Revenue Growth (`Rev_Growth`), and Accrual Ratio.

## 3. Methods
The project workflow consists of two main technical stages:
1. **Data Engineering (Jupyter Notebook):** I used `pandas` for cleaning financial records, handling missing values, and calculating key accounting ratios (e.g., Accrual Ratio via Sloan 1996 methodology). 
2. **Interactive Frontend (Streamlit):** The results were transformed into a web application. I utilized `plotly` for dynamic visualizations, including highlighted scatter plots and interactive bar charts with sector benchmarks.

## 4. Key Findings
* **Firm-Level Heterogeneity:** There is no consistent relationship between high revenue growth and high earnings quality; individual firm performance varies significantly regardless of growth status.
* **Decoupling Risks:** Several "Growth" firms (e.g., BYND) exhibit significant decoupling between Net Income and Operating Cash Flow, indicating lower earnings sustainability.
* **Peer Variance:** Even within a stable sector like Food & Beverage, accrual ratios vary widely, justifying the need for firm-specific diagnostic tools over broad industry averages.

## 5. How to Run
To run this application locally on your machine:
1. Clone this repository.
2. Install the required dependencies:  
   `pip install -r requirements.txt`
3. Launch the Streamlit application:  
   `streamlit run app.py`

## 6. Limitations & Next Steps
* **Sample Size:** The current analysis is limited to 10 selected firms within a 5-year period (2020–2024).
* **Metric Scope:** The tool primarily focuses on accrual-based indicators.
* **Next Steps:** Future versions could integrate live financial APIs (e.g., Yahoo Finance) and expand the sample size to include cross-industry comparisons.

---
*Disclaimer: This project utilized AI assistance (Gemini/ChatGPT) for code optimization, English phrasing refinement, and structural formatting of the documentation.*