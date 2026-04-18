import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. Page Configuration
st.set_page_config(
    page_title="Earnings Quality Auditor Pro", 
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

# Company Profiles Database (Fully English for submission)
COMPANY_PROFILES = {
    "KO": {"name": "The Coca-Cola Company", "type": "Mature Giant", "desc": "Global leader in non-alcoholic beverages with an unparalleled distribution network and iconic brands."},
    "PEP": {"name": "PepsiCo, Inc.", "type": "Mature Giant", "desc": "Diversified giant leading in both snacks (Frito-Lay) and beverages."},
    "MDLZ": {"name": "Mondelēz International", "type": "Mature Giant", "desc": "Leading global snack company specializing in chocolate and biscuits (e.g., Oreo)."},
    "GIS": {"name": "General Mills, Inc.", "type": "Mature Giant", "desc": "Premier food company known for breakfast cereals, yogurt, and convenient meals."},
    "KHC": {"name": "The Kraft Heinz Company", "type": "Mature Giant", "desc": "One of the world's largest food companies, famous for condiments and staples."},
    "MNST": {"name": "Monster Beverage Corporation", "type": "Growth Leader", "desc": "Key energy drink player with strong appeal to younger demographics."},
    "BYND": {"name": "Beyond Meat, Inc.", "type": "High Growth", "desc": "Pioneer in plant-based protein, focusing on meat alternatives."},
    "OTLY": {"name": "Oatly Group AB", "type": "High Growth", "desc": "Swedish leader in oat-based dairy alternatives, driving global trends."},
    "CELH": {"name": "Celsius Holdings, Inc.", "type": "High Growth", "desc": "Produces functional energy drinks designed to burn fat and boost metabolism."},
    "SMPL": {"name": "The Simply Good Foods Company", "type": "High Growth", "desc": "Focuses on nutritious snacks and meal replacements (Atkins/Quest)."}
}

@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_data.csv")
    summary = pd.read_csv("firm_summary.csv")
    return df, summary

try:
    df, firm_summary = load_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# --- 2. SIDEBAR ---
st.sidebar.title("📊 Control Panel")

# Firm A Selection
st.sidebar.subheader("📍 1. Primary Selection (Firm A)")
ticker_list = sorted(df['tic'].unique())
ticker_a = st.sidebar.selectbox("Select Main Firm", ["--- Select a Firm ---"] + ticker_list)

# Firm B Comparison (Optional Toggle)
st.sidebar.subheader("🤝 2. Comparison (Optional)")
enable_comparison = st.sidebar.checkbox("Enable Comparison Mode", value=False)

ticker_b = "None"
if enable_comparison:
    ticker_b = st.sidebar.selectbox("Select Comparison Firm (Firm B)", ["None"] + ticker_list)
    if ticker_b == "None":
        st.sidebar.info("Please select a peer firm to begin comparison.")
else:
    st.sidebar.caption("Comparison mode is currently disabled.")

# Timeline Filter
min_yr = int(df['fyear'].min())
max_yr = int(df['fyear'].max())
year_range = st.sidebar.slider("Timeline Filter", min_yr, max_yr, (min_yr, max_yr))

st.sidebar.divider()

# Audit Settings
st.sidebar.subheader("⚙️ 3. Audit Settings")
corr_threshold = st.sidebar.slider("Alert Threshold (Correlation)", 0.0, 1.0, 0.6)

# FIXED: Re-added the missing caption logic
show_median = st.sidebar.checkbox("Overlay Industry Median Line", value=True)
if show_median:
    st.sidebar.caption("✨ Median line & Highlighting enabled in 'Peer Benchmarking'.")

st.sidebar.divider()
st.sidebar.info("Methodology: Sloan (1996) Accrual Anomaly")

# --- 3. MAIN DASHBOARD ---
st.title("⚖️ Earnings Quality Auditor Pro")

if ticker_a == "--- Select a Firm ---":
    st.markdown("""
        <div class="welcome-card">
            <h1>Professional Financial Audit Dashboard</h1>
            <p style='font-size: 1.1em; color: #555;'>
                Select one primary company from the sidebar to begin. 
                We will analyze the correlation between Net Income and Operating Cash Flow 
                to evaluate the "Earnings Quality" and financial sustainability of the chosen firm.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.subheader("Sector Overview")
    fig_intro = px.scatter(df, x='Rev_Growth', y='Accrual_Ratio', color='Type', 
                         hover_name='tic', size='at', template="plotly_white",
                         labels={'Rev_Growth': 'Revenue Growth', 'Accrual_Ratio': 'Accrual Ratio'})
    st.plotly_chart(fig_intro, use_container_width=True)

else:
    # Data Processing: Firm A
    data_a = df[(df['tic'] == ticker_a) & (df['fyear'].between(year_range[0], year_range[1]))].sort_values('fyear')
    
    if data_a.empty:
        st.warning(f"No data available for {ticker_a} in this period.")
    else:
        correlation_a = data_a['ni'].corr(data_a['oancf']) if len(data_a) > 1 else 0
        latest_accrual_a = data_a['Accrual_Ratio'].iloc[-1]
        avg_accrual_a = data_a['Accrual_Ratio'].mean()

        # Dynamic Audit Banner
        if correlation_a < corr_threshold:
            st.error(f"🔴 **HIGH RISK**: {ticker_a} correlation ({correlation_a:.2f}) is below threshold ({corr_threshold}).")
        else:
            st.success(f"🟢 **AUDIT PASSED**: {ticker_a} maintains healthy earnings quality (Correlation: {correlation_a:.2f}).")

        # Business Profile Expander
        if ticker_a in COMPANY_PROFILES:
            profile = COMPANY_PROFILES[ticker_a]
            with st.expander(f"📖 Business Profile: {profile['name']} ({ticker_a})"):
                st.write(f"**Classification:** {profile['type']}")
                st.write(f"**Overview:** {profile['desc']}")

        # KPI Metrics Row
        c1, c2, c3 = st.columns(3)
        # FIXED: Restored delta_color="inverse" (Higher ratio = Higher risk)
        c1.metric("Latest Accrual Ratio", f"{latest_accrual_a:.4f}", 
                  delta=f"{latest_accrual_a - avg_accrual_a:.4f}", delta_color="inverse")
        c2.metric("NI-OCF Correlation", f"{correlation_a:.2f}")
        c3.metric("Avg Revenue Growth", f"{data_a['Rev_Growth'].mean():.2%}")

        # Analysis Tabs
        tab_titles = ["📈 Financial Trends", "📊 Peer Benchmarking", "🌐 Global Positioning"]
        if enable_comparison and ticker_b != "None":
            tab_titles.append("🤝 Comparative Analysis")
        
        tabs = st.tabs(tab_titles)

        with tabs[0]:
            st.subheader(f"Earnings vs. Cash Flow: {ticker_a}")
            fig_line = go.Figure()
            fig_line.add_trace(go.Scatter(x=data_a['fyear'], y=data_a['ni'], name="Net Income", line=dict(color='#003366', width=4)))
            fig_line.add_trace(go.Scatter(x=data_a['fyear'], y=data_a['oancf'], name="Op. Cash Flow", line=dict(color='#FF4B4B', dash='dot', width=4)))
            fig_line.update_layout(template="plotly_white", hovermode="x unified")
            st.plotly_chart(fig_line, use_container_width=True)

        with tabs[1]:
            st.subheader("Industry Peer Ranking (Avg Accrual Ratio)")
            plot_summary = firm_summary.sort_values('Avg_Accrual_Ratio').copy()
            plot_summary['Highlight'] = plot_summary['tic'].apply(lambda x: 'Selected Firm' if x == ticker_a else 'Industry Average')
            rank_fig = px.bar(plot_summary, x='tic', y='Avg_Accrual_Ratio', color='Highlight',
                              color_discrete_map={'Selected Firm': '#FF4B4B', 'Industry Average': '#D3D3D3'},
                              template="plotly_white")
            
            if show_median:
                median_val = firm_summary['Avg_Accrual_Ratio'].median()
                # FIXED: Restored annotation_position="top left"
                rank_fig.add_hline(y=median_val, line_dash="dash", line_color="#333333", line_width=2,
                                  annotation_text=f"Median: {median_val:.4f}", annotation_position="top left")
            st.plotly_chart(rank_fig, use_container_width=True)

        with tabs[2]:
            st.subheader("Dynamic Positioning within Sector")
            df_plot = df.copy()
            def get_highlight(x):
                if x == ticker_a: return 'Firm A (Target)'
                if enable_comparison and x == ticker_b: return 'Firm B (Compare)'
                return 'Industry Peers'
            df_plot['Highlight'] = df_plot['tic'].apply(get_highlight)
            
            # FIXED: Restored professional axis labels
            fig_global = px.scatter(
                df_plot, x='Rev_Growth', y='Accrual_Ratio', 
                color='Highlight',
                color_discrete_map={'Firm A (Target)': '#FF4B4B', 'Firm B (Compare)': '#003366', 'Industry Peers': '#D3D3D3'},
                hover_name='tic', size='at', template="plotly_white",
                labels={'Rev_Growth': 'Revenue Growth', 'Accrual_Ratio': 'Accrual Ratio'}
            )
            st.plotly_chart(fig_global, use_container_width=True)

        if enable_comparison and ticker_b != "None":
            with tabs[3]:
                st.subheader(f"🤝 Head-to-Head Comparison: {ticker_a} vs {ticker_b}")
                data_b = df[(df['tic'] == ticker_b) & (df['fyear'].between(year_range[0], year_range[1]))].sort_values('fyear')
                corr_b = data_b['ni'].corr(data_b['oancf']) if len(data_b) > 1 else 0

                cola, colb = st.columns(2)
                cola.metric(f"{ticker_a} NI-OCF Corr", f"{correlation_a:.2f}")
                colb.metric(f"{ticker_b} NI-OCF Corr", f"{corr_b:.2f}")

                fig_comp = go.Figure()
                fig_comp.add_trace(go.Scatter(x=data_a['fyear'], y=data_a['Accrual_Ratio'], name=f"{ticker_a}", line=dict(color='#FF4B4B', width=3)))
                fig_comp.add_trace(go.Scatter(x=data_b['fyear'], y=data_b['Accrual_Ratio'], name=f"{ticker_b}", line=dict(color='#003366', width=3)))
                fig_comp.update_layout(yaxis_title="Accrual Ratio", template="plotly_white", hovermode="x unified")
                st.plotly_chart(fig_comp, use_container_width=True)
                st.info("💡 **Comparison Insight:** A widening gap between accrual ratios typically indicates a relative shift in earnings quality.")

        # --- FOOTER: Restored Methodology Expander ---
        st.divider()
        with st.expander("🔬 Statistical Deep Dive & Academic Methodology"):
            col_m, col_f = st.columns(2)
            with col_m:
                st.markdown("**Correlation Matrix (Firm A)**")
                st.write(data_a[['ni', 'oancf', 'Accrual_Ratio', 'Rev_Growth']].corr())
            with col_f:
                st.markdown("**Formula Foundation**")
                st.latex(r"Accrual Ratio = \frac{Net Income - Operating Cash Flow}{Average Total Assets}")
                st.write("Calculated based on Sloan (1996). **High values** suggest that earnings are driven by non-cash accruals rather than real cash flow, implying potential accounting risk.")

st.caption("Data Science Portfolio | ACC102: Financial Analysis | © 2026")