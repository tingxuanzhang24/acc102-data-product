# Earnings Quality Analysis & Interactive Tool (Food & Beverage Sector)

**Product Link:** https://acc102-data-appuct-ryzcejzwsd3xmrmfa8ie6h.streamlit.app/

---

## 1. Problem & User
This project investigates whether revenue growth serves as a reliable indicator of financial risk in the "stable" Food & Beverage sector. It provides an interactive diagnostic tool for **investors and financial analysts** to identify potential "earnings decoupling"—where reported profits are not supported by cash flows.

## 2. Data
* **Source:** WRDS Compustat Database.
* **Access Date:** April 14, 2026.
* **Key Fields:** Net Income (`ni`), Operating Cash Flow (`oancf`), Total Assets (`at`), Revenue Growth (`Rev_Growth`).

## 3. Methods
1. **Data Engineering:** Cleaned and pre-processed financial data using `pandas`, calculating the **Accrual Ratio** based on Sloan’s (1996) methodology.
2. **Analysis:** Performed grouping and statistical trend analysis in a Jupyter Notebook.
3. **Application:** Developed a `Streamlit` dashboard using `plotly` for dynamic firm positioning and sensitivity-based risk auditing.

## 4. Key Findings
* **Label Ineffectiveness:** Traditional "Growth vs. Mature" classifications fail to explain earnings quality variations in this sector.
* **Firm-Level Variance:** Individual corporate governance and accounting practices are more significant than industry-wide trends.
* **Decoupling Risk:** High-growth firms often exhibit lower correlation between profits and cash, necessitating case-by-case auditing.

## 5. How to Run
To run this application locally:
1. Clone the repository and navigate to the folder.
2. Install dependencies: `pip install -r requirements.txt`
3. Launch the app: `streamlit run app.py`

## 6. Product Link / Demo Video
* **Live App:** [Click Here to Access](https://acc102-data-appuct-ryzcejzwsd3xmrmfa8ie6h.streamlit.app/)
* **Demo Video:** [Insert your video link here]

## 7. Limitations & Next Steps
* **Limitations:** Small sample size ($n=10$) and reliance on static historical data (2020–2024).
* **Next Steps:** Integrate real-time Financial APIs (e.g., Yahoo Finance) and expand to cross-sector comparisons (e.g., Tech vs. Consumer Staples).

---
*Disclaimer: AI assistance was used for code optimization and documentation refinement (Reflected in report).*