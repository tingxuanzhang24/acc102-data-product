# ⚖️ Earnings Quality Auditor (Food & Beverage Sector)

## 1. Problem & User

This project develops an interactive **Streamlit** tool based on financial data from the food and beverage industry to explore differences in **earnings quality** across firms and evaluate whether revenue growth can be used as a reliable indicator of financial risk.

**The Challenge:** Firms are often compared using broad labels such as “growth” and “mature.” However, this project finds that these simplified categories do not adequately explain differences in earnings quality. Instead, **firm-level variation** appears to be more important. Therefore, this tool transforms accounting data into an interactive dashboard, allowing **investors and financial analysts** to look beyond top-line growth and identify potential **earnings quality risks** through cash flow analysis.

## 2. Data

- **Source:** WRDS Compustat Database (accessed April 2026).
- **Sample:** 10 food and beverage firms covering the period from 2020 to 2024.
- **Key Fields:** Net Income (`ni`), Operating Cash Flow (`oancf`), Total Assets (`at`), and Revenue (`revt`).
- **Constructed Metrics:** The project calculates **Accruals**, **Accrual Ratio** (based on the Sloan 1996 methodology), and **Revenue Growth** to evaluate earnings sustainability at the individual firm level.

## 3. Methods

The project follows a robust Python-based data pipeline:
1. **Data Preprocessing:** Cleaning WRDS raw data, handling missing values, and standardising fiscal years using **pandas**.
2. **Feature Engineering:** Transforming raw accounting variables into earnings quality indicators, specifically the **Accrual Ratio**.
3. **Analysis:** Examining the relationship between revenue growth and accrual-based quality metrics to identify potential financial anomalies.
4. **Dashboard Development:** Building an interactive tool using **Streamlit** and **Plotly** for multi-firm benchmarking and trend visualisation.

## 4. Key Findings

- **Weak Link Between Growth and Quality:** Revenue growth does not show a clear or consistent relationship with earnings quality in this sample.
- **Limits of Simple Classification:** The difference between “growth” and “mature” firms is not statistically significant, suggesting that these broad labels may not be reliable for risk assessment.
- **Importance of Firm-Level Analysis:** Differences between individual firms are more important than broad group classification when evaluating earnings quality.
- **Risk Signals:** Some firms with strong revenue growth still show weak earnings quality signals, which suggests that growth alone is not enough to assess financial risk.
- **Practical Value:** For decision-making, firm-level accrual analysis provides more useful insight than relying only on revenue growth.

## 5. How to Run

1. **Install dependencies:**
   `pip install -r requirements.txt`

2. **Ensure the following files are in the root directory:**
   - `app.py`
   - `cleaned_data.csv`
   - `firm_summary.csv`

3. **Run the application locally:**
   `streamlit run app.py`

## 6. Product Link / Demo

- **Live App:** https://acc102-data-appuct-ryzcejzwsd3xmrmfa8ie6h.streamlit.app/
- **Demo Video (1–3 min):** [Paste your Mediasite video link here]
- **GitHub Repository:** https://github.com/tingxuanzhang24/acc102-data-product

## 7. Limitations & Next Steps

- **Sample Size:** The study includes only 10 firms, which limits the generalisability of the findings. Future improvements could expand the sample to include more listed food and beverage firms.
- **Time Window:** The 2020–2024 period may not fully capture longer-term financial patterns or industry changes. Extending the time horizon would provide a more robust basis for trend analysis.
- **Additional Indicators:** Future versions could include additional financial indicators to provide a broader assessment of earnings quality and financial risk.

---

**Author:** Tingxuan Zhang 
**Module:** ACC102 Mini Assignment (2025-26 S2)ui Zhang]
**Module:** ACC102 Mini Assignment (2025-26 S2)