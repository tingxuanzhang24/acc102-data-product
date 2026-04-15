import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. Page Configuration
st.set_page_config(
    page_title="Earnings Quality Auditor", 
    page_icon="⚖️", 
    layout="wide"
)

# Custom Professional Styling
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 12px; border: 1px solid #eee; }
    .welcome-card {
        padding: 40px; background-color: #ffffff; border-radius: 12px;
        border-left: 10px solid #003366; box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_data.csv")
    summary = pd.read_csv("firm_summary.csv")
    return df, summary

# Load Data
try:
    df, firm_summary = load_data()
except Exception as e:
    st.error(f"Data loading failed: {e}")
    st.stop()

# --- 2. SIDEBAR: The 'Analytical Remote Control' ---
st.sidebar.title("🎮 Analysis Console")

st.sidebar.subheader("📍 1. Data Selection")
ticker_list = sorted(df['tic'].unique())
ticker = st.sidebar.selectbox("Choose a Firm", ["--- Select a Firm ---"] + ticker_list)
year_range = st.sidebar.slider("Timeline Filter", 2018, 2024, (2020, 2024))

st.sidebar.divider()

st.sidebar.subheader("⚙️ 2. Audit Sensitivity")
# This slider directly controls the Red/Green status on the main page
corr_threshold = st.sidebar.slider(
    "Alert Threshold (Correlation)", 
    min_value=0.0, max_value=1.0, value=0.6,
    help="Determines the minimum NI-OCF correlation required for a 'Healthy' status."
)
show_industry_avg = st.sidebar.checkbox("Overlay Industry Median", value=True)

st.sidebar.divider()
st.sidebar.info("Methodology: Sloan (1996) Accrual Anomaly")
st.sidebar.caption("Data Source: WRDS Compustat")

# --- 3. MAIN DASHBOARD CONTENT ---
st.title("⚖️ Earnings Quality Diagnostic Tool")

if ticker == "--- Select a Firm ---":
    # --- Landing State ---
    st.markdown("""
        <div class="welcome-card">
            <h1>Welcome to the Financial Audit Portal</h1>
            <p style='font-size: 1.2em; color: #555;'>
                High-quality profits are backed by cash flows. Use the <b>Control Panel</b> on the left to select a company and adjust the audit sensitivity.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.subheader("🌐 Global Sector Distribution")
    fig_intro = px.scatter(df, x='Rev_Growth', y='Accrual_Ratio', color='Type', 
                         hover_name='tic', size='at', template="plotly_white")
    st.plotly_chart(fig_intro, use_container_width=True)

else:
    # --- Data Processing for Selected Firm ---
    data = df[(df['tic'] == ticker) & (df['fyear'].between(year_range[0], year_range[1]))].sort_values('fyear')
    
    if data.empty:
        st.warning(f"No data available for {ticker} in the selected time range.")
    else:
        # Core Calculations
        correlation = data['ni'].corr(data['oancf']) if len(data) > 1 else 0
        latest_accrual = data['Accrual_Ratio'].iloc[-1]
        avg_accrual = data['Accrual_Ratio'].mean()

        # --- DYNAMIC DIAGNOSTIC HEADER ---
        # Immediate feedback based on Sidebar Threshold
        if correlation < corr_threshold:
            st.error(f"🔴 **CRITICAL ALERT**: {ticker} shows poor earnings quality. Correlation ({correlation:.2f}) is below your threshold ({corr_threshold}).")
        else:
            st.success(f"🟢 **AUDIT PASSED**: {ticker} maintains healthy earnings quality with strong cash backing (Correlation: {correlation:.2f}).")

        # KPI Metrics Row
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Latest Accrual Ratio", f"{latest_accrual:.4f}", 
                      delta=f"{latest_accrual - avg_accrual:.4f}", delta_color="inverse")
        with col2:
            st.metric("NI-OCF Correlation", f"{correlation:.2f}")
        with col3:
            st.metric("Avg Revenue Growth", f"{data['Rev_Growth'].mean():.2%}")

        # Analysis Workspace
        tab1, tab2, tab3 = st.tabs(["📈 Financial Trends", "📊 Peer Benchmarking", "🔬 Statistical Insights"])
        
        with tab1:
            st.subheader(f"Earnings vs. Cash Flow: {ticker}")
            fig_trends = go.Figure()
            fig_trends.add_trace(go.Scatter(x=data['fyear'], y=data['ni'], name="Net Income", line=dict(color='#003366', width=4)))
            fig_trends.add_trace(go.Scatter(x=data['fyear'], y=data['oancf'], name="Op. Cash Flow", line=dict(color='#FF4B4B', dash='dot', width=4)))
            fig_trends.update_layout(template="plotly_white", hovermode="x unified")
            st.plotly_chart(fig_trends, use_container_width=True)

        with tab2:
            st.subheader("Industry Peer Ranking (Avg Accrual Ratio)")
            rank_fig = px.bar(firm_summary.sort_values('Avg_Accrual_Ratio'), x='tic', y='Avg_Accrual_Ratio', 
                              color='Avg_Accrual_Ratio', color_continuous_scale='RdYlGn_r')
            if show_industry_avg:
                rank_fig.add_hline(y=firm_summary['Avg_Accrual_Ratio'].median(), line_dash="dash", annotation_text="Sector Median")
            st.plotly_chart(rank_fig, use_container_width=True)
            
        with tab3:
            col_m, col_a = st.columns(2)
            with col_m:
                st.markdown("**Correlation Matrix**")
                st.write(data[['ni', 'oancf', 'Accrual_Ratio', 'Rev_Growth']].corr())
            with col_a:
                st.markdown("**Automated Analyst Insight**")
                if correlation < 0.5:
                    st.warning("Analysis: Low correlation suggests profits are largely driven by non-cash adjustments.")
                else:
                    st.info("Analysis: High correlation confirms that net income is supported by genuine cash inflows.")

        # --- Methodology Footer ---
        st.divider()
        with st.expander("📖 Academic Methodology & Calculations"):
            st.markdown("### The Sloan Accrual Anomaly")
            st.latex(r"Accrual Ratio = \frac{Net Income - Operating Cash Flow}{Average Total Assets}")
            st.markdown("""
            **Theory:** Based on Sloan (1996), accruals represent the portion of earnings not yet realized in cash. 
            A high ratio or a decoupling of Profit and Cash (Low Correlation) signals potential earnings management risks.
            """)

st.caption("Data Science Portfolio | ACC102: Financial Data Analysis | © 2026")