import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# 1. Page Configuration
st.set_page_config(
    page_title="Earnings Quality Diagnostic Tool", 
    page_icon="⚖️", 
    layout="wide"
)

# Professional Visual Styling (CSS)
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

df, firm_summary = load_data()

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

# Advanced Analysis Settings
with st.sidebar.expander("🛠️ Analysis Settings", expanded=True):
    min_yr, max_yr = int(df['fyear'].min()), int(df['fyear'].max())
    year_range = st.sidebar.slider("Analysis Timeline", min_yr, max_yr, (min_yr, max_yr))
    
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

if nav_choice == "Deep Analysis":
    if ticker_choice == "--- Select a Firm ---":
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
    else:
        # Data Filtering
        ticker = ticker_choice
        company_data = df[(df['tic'] == ticker) & (df['fyear'].between(year_range[0], year_range[1]))].sort_values('fyear')
        
        # Core Calculations
        correlation = company_data['ni'].corr(company_data['oancf']) if len(company_data) > 1 else 0
        latest_ratio = company_data['Accrual_Ratio'].iloc[-1]
        avg_ratio = company_data['Accrual_Ratio'].mean()

        st.header(f"📈 Financial Health Report: {ticker}")
        
        # Dynamic Diagnostic Header (Keep original logic)
        if correlation < corr_threshold:
            st.error(f"⚠️ **High Alert**: Low Earnings Quality. Profit-Cash decoupling detected (Corr: {correlation:.2f})")
        elif latest_ratio > 0.15:
            st.warning(f"⚠️ **Warning**: Aggressive Accruals detected in the latest period.")
        else:
            st.success(f"✅ **Healthy Profile**: Earnings are strongly backed by operating cash flows.")

        # KPI Metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Latest Accrual Ratio", f"{latest_ratio:.4f}", 
                      delta=f"{latest_ratio - avg_ratio:.4f}", delta_color="inverse")
        with col2:
            st.metric("NI-OCF Correlation", f"{correlation:.2f}")
        with col3:
            st.metric("Avg Rev Growth", f"{company_data['Rev_Growth'].mean():.2%}")

        # Tabs for Depth (Keep original content)
        t1, t2, t3 = st.tabs(["📊 Performance Trends", "🔍 Benchmarking", "🔬 Statistical Insights"])
        
        with t1:
            fig_trends = go.Figure()
            fig_trends.add_trace(go.Scatter(x=company_data['fyear'], y=company_data['ni'], name="Net Income", line=dict(width=4, color='#003366')))
            fig_trends.add_trace(go.Scatter(x=company_data['fyear'], y=company_data['oancf'], name="Op. Cash Flow", line=dict(dash='dot', width=4, color='#FF4B4B')))
            fig_trends.update_layout(template="plotly_white", hovermode="x unified")
            st.plotly_chart(fig_trends, use_container_width=True)

        with t2:
            st.subheader("Industry Peer Ranking")
            rank_fig = px.bar(firm_summary.sort_values('Avg_Accrual_Ratio'), x='tic', y='Avg_Accrual_Ratio', 
                              color='Avg_Accrual_Ratio', color_continuous_scale='RdYlGn_r')
            if show_benchmark:
                rank_fig.add_hline(y=firm_summary['Avg_Accrual_Ratio'].median(), line_dash="dash", line_color="black")
            st.plotly_chart(rank_fig, use_container_width=True)
            
        with t3:
            # Original statistical logic
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown("**Correlation Matrix**")
                st.write(company_data[['ni', 'oancf', 'Accrual_Ratio', 'Rev_Growth']].corr())
            with col_b:
                st.markdown("**Analyst Summary**")
                if correlation < 0.5:
                    st.error(f"Alert: {ticker} shows a weak NI-OCF alignment. This suggests profits may rely on non-cash accruals.")
                else:
                    st.success(f"Insight: {ticker} maintains a solid link between reported profits and cash reality.")

elif nav_choice == "Methodology":
    st.header("📖 Academic Methodology")
    st.latex(r"Accrual Ratio = \frac{Net Income - Operating Cash Flow}{Average Total Assets}")
    st.markdown("""
    Based on **Sloan (1996)**, we evaluate Earnings Quality by checking the 'cash backing' of reported profits. 
    High accruals relative to assets often signal lower future returns and reporting risks.
    """)

else: # Global View with Dynamic Highlighting
    st.header("🌐 Global Industry Distribution")
    st.markdown("Your selected firm is highlighted to show its position within the sector.")
    
    # Dynamic Highlighting Logic
    df['Status'] = df['tic'].apply(lambda x: 'Selected Firm' if x == ticker_choice else 'Industry Peers')
    
    fig_global = px.scatter(
        df, x='Rev_Growth', y='Accrual_Ratio', color='Status',
        color_discrete_map={'Selected Firm': '#FF4B4B', 'Industry Peers': '#003366'},
        hover_name='tic', size='at', template="plotly_white"
    )
    st.plotly_chart(fig_global, use_container_width=True)

st.divider()
st.caption("Data Science Portfolio | ACC102 Financial Analysis Project")