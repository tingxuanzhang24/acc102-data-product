# ⚖️ Earnings Quality Auditor (Food & Beverage Sector)

## 🔗 Live Application & Demo
- **Live App:** https://acc102-data-appuct-ryzcejzwsd3xmrmfa8ie6h.streamlit.app/
- **Demo Video:** [Insert your video link here]

---

## 1. Problem & Target Users

This project investigates earnings quality in the food and beverage industry and examines whether revenue growth can be used as a reliable indicator of financial risk.

Although the sector is generally considered stable, recent years have seen the entry of many emerging firms. This raises the question of whether traditional classifications such as “growth” and “mature” firms can adequately explain differences in earnings quality.

The target users are **investors and financial analysts**, who need to evaluate firm performance beyond simple growth metrics and identify potential financial risks.

---

## 2. Data

- **Source:** WRDS Compustat Database  
- **Access Date:** April 2026  
- **Sample:** 10 food and beverage firms (2020–2024)

### Key Variables:
- Net Income (`ni`)
- Operating Cash Flow (`oancf`)
- Total Assets (`at`)
- Revenue (`revt`)

### Constructed Metrics:
- **Accruals = Net Income – Operating Cash Flow**
- **Accrual Ratio = Accruals / Total Assets**
- **Revenue Growth = Percentage change in revenue**

The dataset is standardised and comparable across firms, making it suitable for firm-level financial analysis.

---

## 3. Methodology

This project combines data analysis with interactive application development:

### Data Processing
- Cleaned and filtered financial data using **Python (pandas)**
- Removed missing values to ensure data quality

### Financial Analysis
- Constructed earnings quality indicators based on **Sloan (1996) Accrual Anomaly**
- Measured:
  - Accrual Ratio (earnings quality proxy)
  - Revenue Growth
  - Correlation between Net Income and Operating Cash Flow

### Statistical Logic
- Compared firms using:
  - Group-level classification (Growth vs. Mature)
  - Firm-level variation analysis
- Used correlation analysis and visualisation to identify patterns

### Application Development
- Built an interactive dashboard using **Streamlit**
- Visualised data using **Plotly**

---

## 4. Key Features (Interactive Tool)

The Streamlit application provides a professional financial audit dashboard:

### 🔹 Firm-Level Analysis
- Select a company to evaluate earnings quality
- View:
  - Net Income vs Operating Cash Flow trends
  - Accrual Ratio metrics
  - Revenue Growth

### 🔹 Risk Detection System
- Dynamic **correlation-based audit signal**
  - Low correlation → potential earnings quality risk
  - High correlation → stronger earnings reliability

### 🔹 Peer Benchmarking
- Compare firms using:
  - Industry ranking (Accrual Ratio)
  - Median benchmark line

### 🔹 Global Positioning
- Scatter plot of:
  - Revenue Growth vs Accrual Ratio
- Visualise firm positioning within the sector

### 🔹 Comparative Analysis (Optional)
- Compare two firms directly
- Identify differences in earnings quality trends

---

## 5. Key Findings

- **No clear relationship** exists between revenue growth and earnings quality  
- **No statistically significant difference** between growth and mature firms  
- **Firm-level variation dominates** industry classification  

This suggests that:

> Earnings quality should be analysed at the **individual firm level**, rather than relying on broad group classifications.

---

## 6. Project Structure

The repository includes:

- `app.py` → Main Streamlit application  
- `notebook.ipynb` → Data cleaning and analysis workflow  
- `cleaned_data.csv` → Processed dataset  
- `firm_summary.csv` → Firm-level summary metrics  
- `requirements.txt` → Python dependencies  
- `README.md` → Project documentation  

---

## 7. How to Run the Project

To run the application locally:

```bash
pip install -r requirements.txt
streamlit run app.py