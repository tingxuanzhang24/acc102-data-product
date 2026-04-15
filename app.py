import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. Page Configuration
st.set_page_config(
    page_title="Earnings Quality & Financial Analysis", 
    page_icon="⚖️", 
    layout="wide"
)

# Custom CSS for a professional look
st.markdown("""
    <style>
    .main { background-color: #f9f9f9; }
    div.stMetric { background-color: #ffffff; padding: 20px; border-radius: 8px; border: 1px solid #e6e6e6; }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    # Ensure these files are in your directory
    df = pd.read_csv("cleaned_data.csv")
    firm_summary = pd.read_csv("firm_summary.csv")
    return df, firm_summary

try:
    df, firm_summary = load_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# --- Sidebar ---
st.sidebar.header("🕹️ Control Panel")
ticker = st.sidebar.selectbox("Select Ticker Symbol:", sorted(df['tic'].unique()))

year_range = st.sidebar.slider(
    "Timeline Selection:",
    int(df['fyear'].min()), int(df['fyear'].max()),
    (int(df['fyear'].min()), int(df['fyear'].max()))
)

# Data Filtering
company_data = df[
    (df['tic'] == ticker) & 
    (df['fyear'].between(year_range[0], year_range[1]))
].sort_values('fyear')

# --- Main Page Header ---
st.title("⚖️ Earnings Quality Explorer")
st.markdown(f"**Enterprise Analysis:** {ticker} | **Industry:** Food & Beverage")

# --- 2. Methodology & Formulas (Expander for High-Score Requirement) ---
with st.expander("📖 View Methodology & Calculation Formulas", expanded=False):
    st.write("To assess earnings quality, we utilize the **Accrual Ratio**. A high ratio suggests that earnings are driven by accounting estimates rather than cash, indicating lower quality.")
    st.latex(r'''
        \text{Accrual Ratio} = \frac{\text{Net Income} - \text{Cash Flow from Operations}}{\text{Average Total Assets}}
    ''')
    st.info("Note: Average Total Assets are calculated based on the beginning and end of the fiscal year.")

# --- 3. Key Performance Indicators (KPIs) ---
col1, col2, col3 = st.columns(3)
with col1:
    avg_accrual = company_data['Accrual_Ratio'].mean()
    st.metric("Avg Accrual Ratio", f"{avg_accrual:.4f}", delta_color="inverse")

with col2:
    avg_growth = company_data['Rev_Growth'].mean()
    st.metric("Avg Revenue Growth", f"{avg_growth:.2%}")

with col3:
    total_ni = company_data['ni'].sum()
    st.metric("Cumulative Net Income", f"${total_ni:,.0f}M")

# --- 4. Interactive Visualization ---
tab1, tab2, tab3 = st.tabs(["📊 Earnings Analysis", "🔍 Industry Benchmarking", "📑 Raw Data"])

with tab1:
    st.subheader("Profitability vs. Cash Flow Realization")
    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(x=company_data['fyear'], y=company_data['ni'], name='Net Income', line=dict(color='#003366', width=3)))
    fig_line.add_trace(go.Scatter(x=company_data['fyear'], y=company_data['oancf'], name='Op. Cash Flow', line=dict(color='#FF4B4B', width=3, dash='dot')))
    fig_line.update_layout(template="plotly_white", hovermode="x unified")
    st.plotly_chart(fig_line, use_container_width=True)

with tab2:
    st.subheader("Sector-wide Accrual Distribution")
    fig_scatter = px.scatter(
        df, x='Rev_Growth', y='Accrual_Ratio', 
        color='Type', hover_name='tic',
        color_discrete_sequence=px.colors.qualitative.Prism
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

with tab3:
    st.subheader("Filtered Financial Statements")
    # Display the raw data table
    st.dataframe(company_data.style.format(precision=2), use_container_width=True)

# --- 5. Advanced Data Insights (Expander) ---
st.divider()
with st.expander("🔬 Advanced Statistical Insights", expanded=True):
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("**Correlation Analysis**")
        corr = company_data[['ni', 'oancf', 'Accrual_Ratio']].corr()
        st.write(corr)
    with col_b:
        st.markdown("**Executive Summary**")
        latest_ratio = company_data['Accrual_Ratio'].iloc[-1]
        status = "Healthy" if latest_ratio < 0.1 else "Investigation Required"
        st.warning(f"Analysis Status: **{status}**")
        st.write(f"The latest Accrual Ratio for {ticker} is {latest_ratio:.4f}. Comparing this to the industry mean allows for a relative assessment of financial reporting aggressiveness.")

st.caption("Data Source: DTS102TC Course Project | Developed for Financial Data Science")