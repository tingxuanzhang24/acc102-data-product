# 📊 Earnings Quality Analysis & Interactive Tool

**🔗 App Link:** [Insert your Streamlit app link here]  
**📺 Demo Video:** [Insert your demo video link here]

---

## 🔍 Overview

This project analyzes earnings quality in the food and beverage industry, a sector typically considered stable and predictable.

Using firm-level financial data from WRDS Compustat (accessed in April 2026), the project examines whether revenue growth is a reliable indicator of financial risk.

The findings show that the relationship between revenue growth and earnings quality is not clear or consistent. While traditional analysis often compares “growth” and “mature” firms, this classification alone does not explain differences in earnings quality. Instead, substantial variation exists across individual firms, even within the same category.

To address this, the analysis is extended into an interactive Streamlit application that allows users to explore firm-level financial performance.

---

## 🎯 Target Users

This project is designed for **investors, financial analysts, and students studying financial analysis** who aim to evaluate company performance beyond simple growth metrics and identify potential financial risks.

---

## 📂 Data Source

- **Source:** WRDS Compustat Database  
- **Access Date:** April 14, 2026  
- **Sample:** 10 firms in the food & beverage industry  
- **Period:** 2020–2024  

**Variables Used:**
- Net Income (`ni`)  
- Operating Cash Flow (`oancf`)  
- Total Assets (`at`)  
- Revenue (`revt`)  

---

## ⚙️ Methodology

### 1. Data Processing
- Removed missing values  
- Sorted by firm and year  
- Calculated key indicators  

### 2. Key Metrics
- **Accruals** = Net Income – Operating Cash Flow  
- **Accrual Ratio** = Accruals / Total Assets  
- **Revenue Growth** = Percentage change in revenue  
*(A higher accrual ratio suggests lower earnings quality.)*

### 3. Firm Classification
Firms are classified into two groups (based on general industry characteristics):
- **Mature firms:** KO, PEP, MDLZ, GIS, KHC  
- **Growth firms:** MNST, BYND, OTLY, CELH, SMPL  

### 4. Analysis Techniques
- Descriptive statistics  
- Firm-level comparison  
- Data visualization  
- Independent sample t-test  

---

## 📊 Key Findings

### 1. No Significant Difference Between Groups
The t-test result shows that the difference in accrual ratios between growth and mature firms is not statistically significant.
👉 *This suggests that growth classification alone does not explain earnings quality.*

### 2. No Clear Relationship Between Growth and Earnings Quality
The scatter plot shows no clear linear relationship between revenue growth and accrual ratio.
👉 *Revenue growth is not a reliable indicator of earnings quality.*

### 3. Strong Firm-Level Differences 
Firm-level analysis reveals substantial variation. Some growth firms (e.g., Oatly, Beyond Meat) show strong earnings quality, while others (e.g., Celsius) show weaker performance.
👉 *Earnings quality varies significantly across individual firms.*

### 💡 4. Final Insight (Conclusion)
**This project demonstrates that relying solely on revenue growth or broad firm classification can be misleading. Instead, firm-level analysis provides more meaningful insights into earnings quality.**

---

## 🚀 Interactive Tool (Streamlit App)

This project includes an interactive tool.

### 🎯 Features
- Select a company (ticker)  
- View: Net Income vs Operating Cash Flow trends, Revenue growth, and Accrual ratio  
- Compare firms using earnings quality ranking  

---

## 📂 Project Structure
```text
project/
│
├── app.py
├── notebook.ipynb
├── cleaned_food_growth_earnings_quality_data.csv
├── firm_summary.csv
├── README.md
└── requirements.txt

--------------------------------------------------------------------------------
▶️ How to Run the App
pip install -r requirements.txt
streamlit run app.py

--------------------------------------------------------------------------------
⚠️ Limitations & Next Steps
Limitations
• Sample Size: The sample size is relatively small, covering only 10 firms.
• Industry Focus: The analysis focuses only on the food and beverage industry, so the findings may not generalize to other sectors.
• Time Period: The time period is limited to 2020–2024.
• Metric Scope: Earnings quality is measured mainly through accrual-based indicators, which may not capture all dimensions of financial risk.
Next Steps
• Expand the sample to include more firms and a longer time period.
• Compare results across multiple industries.
• Incorporate additional financial indicators or regression-based analysis.
• Further improve the interactive tool with richer filtering and comparison functions.