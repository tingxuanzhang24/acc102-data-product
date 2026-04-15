import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# 1. Page Configuration & Visual Enhancement
st.set_page_config(
    page_title="Earnings Quality Diagnostic Tool", 
    page_icon="⚖️", 
    layout="wide"
)

# Professional CSS Styling
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .welcome-card {
        padding: 40px; background-color: #ffffff; border-radius: 12px;
        border-left: 10px solid #003366; box-shadow: 0 4px 12px rgba(0,0,0,0.08);
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

# Error handling for data loading
try:
    df, firm_summary = load_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# --- 2. Enhanced Sidebar: Structured Console ---
st.sidebar.title("📊 Analytics Console")

# Navigation Menu
nav_choice = st.sidebar.radio("Navigation", ["Deep Analysis", "Methodology", "Global Industry View"])

st.sidebar.divider()

# Entity Selection Module
st.sidebar.subheader("🎯 Selection")
sorted_tickers = sorted(df['tic'].unique())
ticker_choice = st.sidebar.selectbox(
    "Select Ticker Symbol", 
    options=["--- Select a Firm ---"] + sorted_tickers
)

# Advanced Analysis Settings Expander
with st.sidebar.expander("🛠️ Analysis Settings", expanded=True):
    # Timeline Slider
    min_yr, max_yr = int(df['fyear'].min()), int(df['fyear'].max())
    year_range = st.sidebar.slider("Analysis Timeline", min_yr, max_yr, (min_yr, max_yr))
    
    # Custom Diagnostic Threshold
    st.markdown("**Diagnostic Sensitivity**")
    corr_threshold = st.slider(
        "Alert Threshold (Correlation)", 
        0.0, 1.0, 0.5, 
        help="Alerts trigger if NI-OCF correlation falls below this value."
    )
    
    show_benchmark = st.checkbox("Overlay Industry Median", value=True)

st.sidebar.divider()
st.sidebar.info(f"Data Source: WRDS Compustat\nLast Updated: April 2026")

# --- 3. Main Content Logic ---

# PAGE A: Deep Analysis
if nav_choice == "Deep Analysis":
    if ticker_choice == "--- Select a Firm ---":
        # Professional Empty State
        st.markdown("""
            <div class="welcome-card">
                <h1>🔍 Earnings Quality Diagnostic Tool</h1>
                <p style='font-size: 1.2em; color: #555;'>
                    Please select a firm from the <b>Selection</b> panel on the left to begin your audit.
                </p>
                <hr>
                <p>High-quality earnings are backed by actual cash flows. This tool uses <b>Accrual Ratio</b> and 
                <b>Statistical Correlations</b> to detect potential financial reporting risks.</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Space-filler Chart
        st.subheader("🌐 Global Sector Distribution (Overview)")
        fig_intro = px.scatter(df, x='Rev_Growth', y='Accrual_Ratio', color='Type', 
                             hover_name='tic', template="plotly_white", size='at')
        st.plotly_chart(fig_intro, use_container_width=True)

    else:
        # --- ANALYSIS STATE ---
        ticker = ticker_choice
        company_data = df[(df['tic'] == ticker) & (df['fyear'].between(year_range[0], year_range[1]))].sort_values('fyear')
        
        # Calculations
        correlation = company_data['ni'].corr(company_data['oancf']) if len(company_data) > 1 else 0
        latest_ratio = company_data['Accrual_Ratio'].iloc[-1]
        avg_ratio = company_data['Accrual_Ratio'].mean()

        st.header(f"📈 Financial Health Report: {ticker}")
        
        # Dynamic Diagnostic Header
        if correlation < corr_threshold:
            st.error(f"⚠️ **High Alert**: Low Earnings Quality. Profit-Cash decoupling detected (Correlation: {correlation:.2f})")
        elif latest_ratio > 0.15:
            st.warning(f"⚠️ **Warning**: Aggressive Accruals detected in the latest fiscal year.")
        else:
            st.success(f"✅ **Healthy Profile**: Earnings are strongly backed by operating cash flows.")

        # KPI Metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Latest Accrual Ratio", f"{latest_ratio:.4f}", 
                      delta=f"{latest_ratio - avg_ratio:.4f}", delta_color="inverse")
        with col2:
            st.metric("NI-OCF Correlation", f"{correlation:.2f}", help="Standard Benchmark: > 0.7")
        with col3:
            st.metric("Avg Rev Growth", f"{company_data['Rev_Growth'].mean():.2%}")

        # Tabs for detailed viewing
        t1, t2, t3 = st.tabs(["📊 Performance Trends", "🔍 Benchmarking", "🔬 Statistical Insights"])
        
        with t1:
            st.subheader("Net Income vs. Operating Cash Flow")
            fig_trends = go.Figure()
            fig_trends.add_trace(go.Scatter(x=company_data['fyear'], y=company_data['ni'], name="Net Income", line=dict(width=4, color='#003366')))
            fig_trends.add_trace(go.Scatter(x=company_data['fyear'], y=company_data['oancf'], name="Op. Cash Flow", line=dict(dash='dot', width=4, color='#FF4B4B')))
            fig_trends.update_layout(template="plotly_white", hovermode="x unified")
            st.plotly_chart(fig_trends, use_container_width=True)

        with t2:
            st.subheader("Industry Peer Ranking (Accrual Ratio)")
            rank_fig = px.bar(firm_summary.sort_values('Avg_Accrual_Ratio'), x='tic', y='Avg_Accrual_Ratio', 
                              color='Avg_Accrual_Ratio', color_continuous_scale='RdYlGn_r')
            if show_benchmark:
                median_val = firm_summary['Avg_Accrual_Ratio'].median()
                rank_fig.add_hline(y=median_val, line_dash="dash", line_color="black", annotation_text="Industry Median")
            st.plotly_chart(rank_fig, use_container_width=True)
            
        with t3:
            st.markdown("**Dynamic Correlation Matrix**")
            st.write(company_data[['ni', 'oancf', 'Accrual_Ratio', 'Rev_Growth']].corr())
            
            # Dynamic Summary Text
            st.markdown("**Analyst Summary**")
            if correlation < 0.5:
                st.error(f"Alert: {ticker} shows a weak NI-OCF alignment. This suggests profits may rely on non-cash accruals.")
            else:
                st.success(f"Insight: {ticker} maintains a solid link between reported profits and cash reality.")

# PAGE B: Methodology
elif nav_choice == "Methodology":
    st.header("📖 Academic Methodology & Context")
    st.write("Our diagnostic engine is based on the **Sloan (1996) Accrual Anomaly** theory.")
    st.latex(r"Accrual Ratio = \frac{Net Income - Operating Cash Flow}{Average Total Assets}")
    st.markdown("""
    ### Why this matters:
    - **Accruals** represent the non-cash component of earnings. 
    - **Sloan's Finding:** Firms with high accrual-to-asset ratios tend to have lower subsequent stock returns and more frequent earnings restatements.
    - **Our Correlation Metric:** Measures the "cash backing" of every dollar of net income.
    """)

# PAGE C: Global View
else:
    st.header("🌐 Global Industry Distribution")
    st.markdown("Use this view to compare all firms in the sector across Growth and Quality dimensions.")
    fig_global = px.scatter(df, x='Rev_Growth', y='Accrual_Ratio', color='Type', 
                           hover_name='tic', size='at', template="plotly_white",
                           labels={'Rev_Growth': 'Revenue Growth (%)', 'Accrual_Ratio': 'Accrual Ratio'})
    st.plotly_chart(fig_global, use_container_width=True)

st.divider()
st.caption("Developed for ACC102: Data Science in Financial Analysis | © 2026")