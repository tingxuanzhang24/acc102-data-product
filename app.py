import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# 1. Page Config
st.set_page_config(page_title="Earnings Quality Explorer", page_icon="⚖️", layout="wide")

# Professional CSS
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .welcome-card {
        padding: 40px; background-color: #ffffff; border-radius: 12px;
        border-left: 8px solid #003366; box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    div.stMetric { 
        background-color: #ffffff; padding: 20px; border-radius: 10px; border: 1px solid #e9ecef; 
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_data.csv")
    firm_summary = pd.read_csv("firm_summary.csv")
    return df, firm_summary

df, firm_summary = load_data()

# --- 2. Sidebar ---
st.sidebar.header("🕹️ Control Panel")
sorted_tickers = sorted(df['tic'].unique())
selection_options = ["--- Please Select a Company ---"] + sorted_tickers

ticker_choice = st.sidebar.selectbox("Step 1: Select a Ticker Symbol", options=selection_options, index=0)

# --- 3. Main Logic ---
st.title("⚖️ Earnings Quality Explorer")

if ticker_choice == "--- Please Select a Company ---":
    st.markdown("""
        <div class="welcome-card">
            <h1>👋 Welcome to the Financial Analysis Portal</h1>
            <p style='font-size: 1.1em;'>Please select a firm from the sidebar to unlock <b>Deep Statistical Analysis</b> and <b>Health Diagnostics</b>.</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.subheader("🌐 Global Sector Overview")
    fig_global = px.scatter(df, x='Rev_Growth', y='Accrual_Ratio', color='Type', hover_name='tic', template="plotly_white")
    st.plotly_chart(fig_global, use_container_width=True)

else:
    ticker = ticker_choice
    year_range = st.sidebar.slider("Step 2: Timeline:", int(df['fyear'].min()), int(df['fyear'].max()), (int(df['fyear'].min()), int(df['fyear'].max())))
    
    # Filter Data
    company_data = df[(df['tic'] == ticker) & (df['fyear'].between(year_range[0], year_range[1]))].sort_values('fyear')

    # --- DYNAMIC ANALYSIS ENGINE ---
    latest_ratio = company_data['Accrual_Ratio'].iloc[-1]
    avg_ratio = company_data['Accrual_Ratio'].mean()
    # Calculate Correlation between NI and OCF (High correlation = High Quality)
    correlation = company_data['ni'].corr(company_data['oancf']) if len(company_data) > 1 else 0

    # Determine Health Status
    if latest_ratio < 0.1 and correlation > 0.7:
        status_msg, status_color = "✅ Robust Earnings Quality", "green"
    elif latest_ratio > 0.15:
        status_msg, status_color = "⚠️ Aggressive Accruals Detected", "orange"
    else:
        status_msg, status_color = "📊 Moderate Financial Position", "blue"

    st.markdown(f"## Analysis for: **{ticker}**")
    st.markdown(f"**Diagnostic Result:** <span style='color:{status_color}; font-weight:bold; font-size:1.2em;'>{status_msg}</span>", unsafe_allow_html=True)

    # KPIs
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Latest Accrual Ratio", f"{latest_ratio:.4f}", delta=f"{latest_ratio - avg_ratio:.4f}", delta_color="inverse")
    with col2:
        st.metric("Avg Rev Growth", f"{company_data['Rev_Growth'].mean():.2%}")
    with col3:
        st.metric("NI-OCF Correlation", f"{correlation:.2f}")

    # Tabs
    tab1, tab2, tab3 = st.tabs(["📈 Financial Trends", "🔍 Benchmarking", "📑 Data View"])
    
    with tab1:
        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(x=company_data['fyear'], y=company_data['ni'], name='Net Income', line=dict(color='#003366', width=3)))
        fig_line.add_trace(go.Scatter(x=company_data['fyear'], y=company_data['oancf'], name='Op. Cash Flow', line=dict(color='#FF4B4B', width=3, dash='dot')))
        fig_line.update_layout(template="plotly_white", hovermode="x unified", title=f"Profit vs Cash Flow for {ticker}")
        st.plotly_chart(fig_line, use_container_width=True)

    with tab2:
        st.subheader("Industry Peer Ranking")
        rank_fig = px.bar(firm_summary.sort_values('Avg_Accrual_Ratio'), x='tic', y='Avg_Accrual_Ratio', color='Avg_Accrual_Ratio', color_continuous_scale='RdYlGn_r')
        st.plotly_chart(rank_fig, use_container_width=True)

    with tab3:
        st.dataframe(company_data.style.format(precision=2), use_container_width=True)

    # --- UPDATED DYNAMIC INSIGHTS ---
    st.divider()
    with st.expander("🔬 Advanced Statistical Insights (Automated Analysis)", expanded=True):
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("**Financial Correlation Matrix**")
            st.write(company_data[['ni', 'oancf', 'Accrual_Ratio', 'Rev_Growth']].corr())
        with col_b:
            st.markdown("**Analyst Summary**")
            # Custom logic per company
            if correlation < 0.5:
                st.error(f"Alert: {ticker} shows a weak correlation ({correlation:.2f}) between Net Income and Cash Flow. This may indicate non-cash earnings.")
            else:
                st.success(f"Stability: {ticker} shows a strong alignment between earnings and cash flows.")
            
            if latest_ratio > avg_ratio:
                st.warning(f"Trend Warning: The current Accrual Ratio is higher than the historical average for {ticker}.")

st.caption("Data Science Portfolio | Financial Data Science Project")