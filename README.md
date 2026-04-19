# Earnings Quality Auditor (Food & Beverage Sector)

## 1. Problem & User

This project develops an interactive Streamlit tool based on financial data from the food and beverage industry to explore differences in earnings quality across firms and evaluate whether revenue growth can be used as a reliable indicator of financial risk.

Traditional analysis often compares “growth” firms with “mature” firms. However, this project finds that such a simple classification does not explain differences in earnings quality very well. Instead, firm-level differences appear to be more important. Therefore, the project not only conducts data analysis but also transforms the results into an interactive tool that allows users to explore firm performance directly and generate more meaningful insights.

The core questions are: how does earnings quality vary across firms in the food and beverage industry, and can revenue growth serve as a reliable signal of financial risk?

The target users are investors and financial analysts who need to compare firms, identify potential financial risk, and assess earnings quality beyond simple growth labels.

## 2. Data

The project uses firm-level financial data from the WRDS Compustat Database, accessed in April 2026. The sample includes 10 food and beverage firms covering the period from 2020 to 2024. The main variables are Net Income (`ni`), Operating Cash Flow (`oancf`), Total Assets (`at`), Revenue (`revt`), Ticker (`tic`), Company Name (`conm`), and Fiscal Year (`fyear`). Based on these variables, the project constructs Accruals, Accrual Ratio, and Revenue Growth to evaluate earnings quality at the firm level.

## 3. Methods

The project was developed using Python for data cleaning, transformation, analysis, and visualisation. The main workflow includes loading firm-level financial data, removing missing values in key variables, constructing accrual-based indicators, calculating revenue growth, generating firm-level summary statistics, and exporting cleaned datasets for the application. The final output is an interactive Streamlit dashboard that allows users to explore earnings quality signals, compare firms, and interpret risk patterns more clearly.

## 4. Key Findings

- Revenue growth does not show a clear or consistent relationship with earnings quality in this sample.
- The difference between “growth” and “mature” firms is not statistically significant.
- Firm-level variation is more important than broad category-based classification.
- Some firms with relatively strong revenue growth still display weak earnings quality signals.
- For practical decision-making, accrual-based firm-level analysis appears more useful than relying only on simple growth labels.

## 5. How to Run

1. Install the required packages:

   `pip install -r requirements.txt`

2. Make sure the following files are in the same folder:

   - `app.py`
   - `cleaned_data.csv`
   - `firm_summary.csv`

3. Run the Streamlit application locally:

   `streamlit run app.py`

The app should then open in your local browser.

## 6. Product Link / Demo

- Live App: https://acc102-data-appuct-ryzcejzwsd3xmrmfa8ie6h.streamlit.app/
- Demo Video (1–3 min): [Paste your demo video link here]
- GitHub Repository: [Paste your repository link here]

## 7. Limitations & Next Steps

This project has several limitations. The sample only includes 10 firms, which limits the generalisability of the findings. The time period from 2020 to 2024 is relatively short and may not fully capture longer-term financial patterns. In addition, the analysis focuses on a limited set of accounting-based indicators and does not include broader market or operational variables. Future improvements could include expanding the sample, extending the time horizon, incorporating additional financial indicators, and improving the dashboard with more user-controlled features and export options.