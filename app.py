import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. Page Configuration
st.set_page_config(
    page_title="Earnings Quality Explorer", 
    page_icon="⚖️", 
    layout="wide"
)

# Professional CSS Styling
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .welcome-card {
        padding: 40px;
        background-color: #ffffff;
        border-radius: 12px;
        border-left: 8px solid #003366;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 25px;
    }
    div.stMetric { 
        background-color: #ffffff; 
        padding: 20px; 
        border-radius: 10px; 
        border: 1px solid #e9ecef; 
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    # Loading datasets from project directory
    df = pd.read_csv("cleaned_data.csv")
    firm_summary = pd.read_csv("firm_summary.csv")
    return df, firm_summary

try:
    df, firm_summary = load_data()
except Exception as e:
    st.error(f"Data loading error: {e}")
    st.stop()

# --- 2. Sidebar with Step-by-Step Logic ---
st.sidebar.header("🕹️ Control Panel")

# Step 1: Company Selection (With a Null start)
sorted_tickers = sorted(df['tic'].unique())
selection_options = ["--- Please Select a Company ---"] + sorted_tickers

ticker_choice = st.sidebar.selectbox(
    "Step 1: Select a Ticker Symbol", 
    options=selection_options,
    index=0
)

# --- 3. Main Logic: Conditional Rendering ---
st.title("⚖️ Earnings Quality Explorer")

if ticker_choice == "--- Please Select a Company ---":
    # --- LANDING STATE (Welcome Screen) ---
    st.markdown("""
        <div class="welcome-card">
            <h1>👋 Welcome to the Financial Analysis Portal</h1>
            <p style='font-size: 1.2em; color: #555;'>
                This application assesses the <b>Earnings Quality</b> of firms within the Food & Beverage industry. 
                High-quality earnings are those that are backed by actual cash flows rather than aggressive accounting accruals.
            </p>
            <hr>
            <p><b>To begin your analysis:</b> Please select a company ticker from the sidebar on the left.</p>
        </div>
    """, unsafe_allow_html=True)

    # Global Industry Chart to fill the space professionally
    st.subheader("🌐 Global Industry Distribution (Sector-wide)")
    fig_global = px.scatter(
        df, x='Rev_Growth', y='Accrual_Ratio', color='Type', 
        hover_name='tic', title="Revenue Growth vs. Accrual Ratio (All Firms)",
        labels={'Rev_Growth': 'Revenue Growth (%)', 'Accrual_Ratio': 'Accrual Ratio'}
    )
    fig_global.update_layout(template="plotly_white")
    st.plotly_chart(fig_global, use_container_width=True)

else:
    # --- ANALYSIS STATE (Firm Specific) ---
    ticker = ticker_choice
    
    # Step 2: Enable Timeline Slider only after selection
    year_range = st.sidebar.slider(
        "Step 2: Selection Timeline:",
        int(df['fyear'].min()), int(df['fyear'].max()),
        (int(df['fyear'].min()), int(df['fyear'].max()))
    )

    # Filter Data
    company_data = df[
        (df['tic'] == ticker) & 
        (df['fyear'].between(year_range[0], year_range[1]))
    ].sort_values('fyear')

    st.markdown(f"## 📈 Comprehensive Analysis for: **{ticker}**")
    
    # Methodology Expander
    with st.expander("📖 View Methodology & Formulas", expanded=False):
        st.write("We use the **Accrual Ratio** to detect earnings management. Lower ratios suggest higher earnings quality.")
        st.latex(r"\text{Accrual Ratio} = \frac{\text{Net Income} - \text{Cash Flow from Operations}}{\text{Average Total Assets}}")

    # KPIs
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Avg Accrual Ratio", f"{company_data['Accrual_Ratio'].mean():.4f}")
    with col2:
        st.metric("Avg Rev Growth", f"{company_data['Rev_Growth'].mean():.2%}")
    with col3:
        latest_ni = company_data['ni'].iloc[-1]
        st.metric("Latest Net Income", f"${latest_ni:,.0f}M")

    # Tabs for Organization
    tab1, tab2, tab3 = st.tabs(["📊 Performance Charts", "🔍 Industry Benchmarking", "📑 Raw Data"])
    
    with tab1:
        st.subheader("Net Income vs. Operating Cash Flow")
        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(x=company_data['fyear'], y=company_data['ni'], name='Net Income', line=dict(color='#003366', width=3)))
        fig_line.add_trace(go.Scatter(x=company_data['fyear'], y=company_data['oancf'], name='Op. Cash Flow', line=dict(color='#FF4B4B', width=3, dash='dot')))
        fig_line.update_layout(template="plotly_white", hovermode="x unified")
        st.plotly_chart(fig_line, use_container_width=True)

    with tab2:
        st.subheader("Firm Ranking by Accrual Ratio")
        rank_fig = px.bar(firm_summary.sort_values('Avg_Accrual_Ratio'), x='tic', y='Avg_Accrual_Ratio', color='Avg_Accrual_Ratio', color_continuous_scale='RdYlGn_r')
        st.plotly_chart(rank_fig, use_container_width=True)

    with tab3:
        st.subheader("Filtered Financial Statement Data")
        st.dataframe(company_data.style.format(precision=2), use_container_width=True)

    # Statistical Insights Expander
    st.divider()
    with st.expander("🔬 Advanced Statistical Insights", expanded=True):
        st.success(f"Analytical Insight: Differences across firms like {ticker} are statistically more significant than growth classification alone.")

st.caption("Data Source: DTS102TC Course Project | Developed for Financial Data Science")