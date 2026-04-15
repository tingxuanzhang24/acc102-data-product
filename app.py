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

# Professional Visual Styling
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
    # Ensure these filenames match your uploaded files exactly
    df = pd.read_csv("cleaned_data.csv")
    summary = pd.read_csv("firm_summary.csv")
    return df, summary

try:
    df, firm_summary = load_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# --- 2. SIDEBAR: The Analytical Remote Control ---
st.sidebar.title("📊 Control Panel")

st.sidebar.subheader("📍 1. Selection")
ticker_list = sorted(df['tic'].unique())
ticker = st.sidebar.selectbox("Choose a Firm", ["--- Select a Firm ---"] + ticker_list)

# DYNAMIC TIME FILTER: Automatically detects 2020-2024 from your data
min_yr = int(df['fyear'].min())
max_yr = int(df['fyear'].max())
year_range = st.sidebar.slider("Timeline Filter", min_yr, max_yr, (min_yr, max_yr))

st.sidebar.divider()

st.sidebar.subheader("⚙️ 2. Audit Settings")
# Slider to control the Red/Green Status Banner
corr_threshold = st.sidebar.slider(
    "Alert Threshold (Correlation)", 
    0.0, 1.0, 0.6,
    help="Determines the minimum NI-OCF correlation for a 'Healthy' status."
)

# Checkbox for the Median Line in Tab 2
show_median = st.sidebar.checkbox("Overlay Industry Median Line", value=True)
if show_median:
    st.sidebar.caption("✨ Median line enabled in 'Peer Benchmarking' tab.")

st.sidebar.divider()
st.sidebar.info("Methodology: Sloan (1996) Accrual Anomaly")

# --- 3. MAIN DASHBOARD ---
st.title("⚖️ Financial Health & Earnings Quality Auditor")

if ticker == "--- Select a Firm ---":
    # --- Landing Page ---
    st.markdown("""
        <div class="welcome-card">
            <h1>Welcome to the Professional Audit Portal</h1>
            <p style='font-size: 1.1em; color: #555;'>
                High-quality earnings are backed by actual cash flows. Select a company from the <b>Control Panel</b> 
                to analyze its financial health and adjust audit sensitivity.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.subheader("Sector Overview")
    fig_intro = px.scatter(df, x='Rev_Growth', y='Accrual_Ratio', color='Type', 
                         hover_name='tic', size='at', template="plotly_white")
    st.plotly_chart(fig_intro, use_container_width=True)

else:
    # --- Data Processing for Selected Firm ---
    data = df[(df['tic'] == ticker) & (df['fyear'].between(year_range[0], year_range[1]))].sort_values('fyear')
    
    if data.empty:
        st.warning("No data available for the selected period.")
    else:
        # Core Statistics
        correlation = data['ni'].corr(data['oancf']) if len(data) > 1 else 0
        latest_accrual = data['Accrual_Ratio'].iloc[-1]
        avg_accrual = data['Accrual_Ratio'].mean()

        # --- DYNAMIC AUDIT BANNER ---
        if correlation < corr_threshold:
            st.error(f"🔴 **HIGH RISK**: {ticker} correlation ({correlation:.2f}) is below your threshold ({corr_threshold}).")
        else:
            st.success(f"🟢 **AUDIT PASSED**: {ticker} maintains healthy earnings quality (Correlation: {correlation:.2f}).")

        # KPI Metrics Row
        c1, c2, c3 = st.columns(3)
        c1.metric("Latest Accrual Ratio", f"{latest_accrual:.4f}", 
                  delta=f"{latest_accrual - avg_accrual:.4f}", delta_color="inverse")
        c2.metric("NI-OCF Correlation", f"{correlation:.2f}")
        c3.metric("Avg Revenue Growth", f"{data['Rev_Growth'].mean():.2%}")

        # Analysis Tabs
        tab1, tab2, tab3 = st.tabs(["📈 Financial Trends", "📊 Peer Benchmarking", "🌐 Global Positioning"])
        
        with tab1:
            st.subheader(f"Earnings vs. Cash Flow: {ticker}")
            fig_line = go.Figure()
            fig_line.add_trace(go.Scatter(x=data['fyear'], y=data['ni'], name="Net Income", line=dict(color='#003366', width=4)))
            fig_line.add_trace(go.Scatter(x=data['fyear'], y=data['oancf'], name="Op. Cash Flow", line=dict(color='#FF4B4B', dash='dot', width=4)))
            fig_line.update_layout(template="plotly_white", hovermode="x unified")
            st.plotly_chart(fig_line, use_container_width=True)

        with tab2:
            st.subheader("Industry Peer Ranking (Accrual Ratio)")
            rank_fig = px.bar(firm_summary.sort_values('Avg_Accrual_Ratio'), x='tic', y='Avg_Accrual_Ratio', 
                              color='Avg_Accrual_Ratio', color_continuous_scale='RdYlGn_r')
            
            # --- CLEAR & BOLD MEDIAN LINE ---
            if show_median:
                median_val = firm_summary['Avg_Accrual_Ratio'].median()
                rank_fig.add_hline(
                    y=median_val, 
                    line_dash="dash", 
                    line_color="#333333", 
                    line_width=2,
                    annotation_text=f"Industry Median: {median_val:.4f}", 
                    annotation_position="top left"
                )
            st.plotly_chart(rank_fig, use_container_width=True)

        with tab3:
            st.subheader("Dynamic Highlighting within Sector")
            # Create a status column for dynamic highlighting
            df_plot = df.copy()
            df_plot['Highlight'] = df_plot['tic'].apply(lambda x: 'Selected Firm' if x == ticker else 'Industry Peers')
            
            fig_global = px.scatter(
                df_plot, x='Rev_Growth', y='Accrual_Ratio', 
                color='Highlight',
                color_discrete_map={'Selected Firm': '#FF4B4B', 'Industry Peers': '#003366'},
                hover_name='tic', size='at', template="plotly_white",
                labels={'Rev_Growth': 'Revenue Growth', 'Accrual_Ratio': 'Accrual Ratio'}
            )
            st.plotly_chart(fig_global, use_container_width=True)

        # --- FOOTER: STATS & METHODOLOGY ---
        st.divider()
        with st.expander("🔬 Statistical Deep Dive & Academic Methodology"):
            col_m, col_f = st.columns(2)
            with col_m:
                st.markdown("**Correlation Matrix**")
                st.write(data[['ni', 'oancf', 'Accrual_Ratio', 'Rev_Growth']].corr())
            with col_f:
                st.markdown("**Formula Foundation**")
                st.latex(r"Accrual Ratio = \frac{Net Income - Operating Cash Flow}{Average Total Assets}")
                st.write("Sloan (1996) implies that high accruals often precede future earnings reversals.")

st.caption("Data Science Portfolio | ACC102: Financial Analysis | © 2026")