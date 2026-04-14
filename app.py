import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Earnings Quality Explorer", layout="wide")

st.title("📊 Earnings Quality Explorer")
st.write("Explore firm-level earnings quality in the food & beverage industry.")

@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_data.csv")
    firm_summary = pd.read_csv("firm_summary.csv")
    return df, firm_summary

df, firm_summary = load_data()

st.sidebar.header("🔍 Select Company")
ticker = st.sidebar.selectbox("Choose a firm:", sorted(df['tic'].unique()))

company_data = df[df['tic'] == ticker].sort_values('fyear')

st.subheader("📌 Key Metrics")

col1, col2 = st.columns(2)
col1.metric("Average Accrual Ratio", f"{company_data['Accrual_Ratio'].mean():.4f}")
col2.metric("Average Revenue Growth", f"{company_data['Rev_Growth'].mean():.4f}")

st.subheader("📈 Net Income vs Operating Cash Flow")

fig, ax = plt.subplots()
ax.plot(company_data['fyear'], company_data['ni'], marker='o', label='Net Income')
ax.plot(company_data['fyear'], company_data['oancf'], marker='o', label='Operating Cash Flow')
ax.set_xlabel("Year")
ax.set_ylabel("Value")
ax.legend()
st.pyplot(fig)

st.subheader("📊 Growth vs Earnings Quality")

plot_df = df.dropna(subset=['Rev_Growth', 'Accrual_Ratio'])

fig2, ax2 = plt.subplots()
for t in plot_df['Type'].unique():
    subset = plot_df[plot_df['Type'] == t]
    ax2.scatter(subset['Rev_Growth'], subset['Accrual_Ratio'], label=t, alpha=0.7)

ax2.axhline(0, linestyle='--')
ax2.set_xlabel("Revenue Growth")
ax2.set_ylabel("Accrual Ratio")
ax2.legend()
st.pyplot(fig2)

st.subheader("🏆 Earnings Quality Ranking")

rank = firm_summary.sort_values('Avg_Accrual_Ratio')

fig3, ax3 = plt.subplots()
ax3.bar(rank['tic'], rank['Avg_Accrual_Ratio'])
ax3.axhline(0, linestyle='--')
ax3.set_xlabel("Company")
ax3.set_ylabel("Average Accrual Ratio")
ax3.set_title("Firm-Level Ranking")
st.pyplot(fig3)

st.subheader("💡 Key Insight")
st.info(
    "The analysis shows no clear relationship between revenue growth and earnings quality. "
    "Differences across individual firms are more significant than growth classification."
)