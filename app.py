import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. Page Configuration
st.set_page_config(page_title="Earnings Quality Auditor", page_icon="⚖️", layout="wide")

# Professional CSS
st.markdown("""
    <style>
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; border: 1px solid #eee; }
    .welcome-card { padding: 30px; background-color: #ffffff; border-radius: 12px; border-left: 8px solid #003366; }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_data.csv")
    summary = pd.read_csv("firm_summary.csv")
    return df, summary

df, firm_summary = load_data()

# --- 2. SIDEBAR: The Remote Control ---
st.sidebar.title("📊 Control Panel")

st.sidebar.subheader("📍 1. Selection")
ticker = st.sidebar.selectbox("Choose a Firm", ["--- Select ---"] + sorted(df['tic'].unique()))
year_range = st.sidebar.slider("Timeline Filter", 2018, 2024, (2020, 2024))

st.sidebar.divider()

st.sidebar.subheader("⚙️ 2. Audit Settings")
# 阈值滑块：控制顶部横幅颜色
corr_threshold = st.sidebar.slider("Diagnostic Sensitivity (Corr)", 0.0, 1.0, 0.6)

# 优化后的基准线勾选：增加明确的提示
show_median = st.sidebar.checkbox("Overlay Industry Median Line", value=True)
if show_median:
    st.sidebar.caption("✨ Line added to 'Peer Benchmarking' tab.")

st.sidebar.divider()
st.sidebar.info("Methodology: Sloan (1996) Accrual Anomaly")

# --- 3. MAIN CONTENT ---
st.title("⚖️ Financial Health Audit Dashboard")

if ticker == "--- Select ---":
    st.markdown("""
        <div class="welcome-card">
            <h2>Welcome to the Audit Portal</h2>
            <p>Please select a company on the left to analyze its earnings quality. 
            Adjust the <b>Control Panel</b> to set your own audit sensitivity.</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.subheader("Sector Overview")
    fig_init = px.scatter(df, x='Rev_Growth', y='Accrual_Ratio', color='Type', hover_name='tic', template="plotly_white")
    st.plotly_chart(fig_init, use_container_width=True)

else:
    # Data Processing
    data = df[(df['tic'] == ticker) & (df['fyear'].between(year_range[0], year_range[1]))].sort_values('fyear')
    correlation = data['ni'].corr(data['oancf']) if len(data) > 1 else 0
    latest_accrual = data['Accrual_Ratio'].iloc[-1]
    avg_accrual = data['Accrual_Ratio'].mean()

    # --- DYNAMIC HEADER ---
    if correlation < corr_threshold:
        st.error(f"🔴 **HIGH RISK**: {ticker} correlation ({correlation:.2f}) is below your threshold ({corr_threshold}).")
    else:
        st.success(f"🟢 **HEALTHY**: {ticker} passes the audit with correlation ({correlation:.2f}).")

    # Metrics
    c1, c2, c3 = st.columns(3)
    c1.metric("Latest Accrual Ratio", f"{latest_accrual:.4f}", 
              delta=f"{latest_accrual - avg_accrual:.4f}", delta_color="inverse")
    c2.metric("NI-OCF Correlation", f"{correlation:.2f}")
    c3.metric("Avg Growth", f"{data['Rev_Growth'].mean():.2%}")

    # Tabs
    tab1, tab2, tab3 = st.tabs(["📈 Trends", "📊 Peer Benchmarking", "🌐 Global Positioning"])
    
    with tab1:
        st.subheader("Net Income vs. Cash Flow")
        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(x=data['fyear'], y=data['ni'], name="Net Income", line=dict(color='#003366', width=4)))
        fig_line.add_trace(go.Scatter(x=data['fyear'], y=data['oancf'], name="Cash Flow", line=dict(color='#FF4B4B', dash='dot', width=4)))
        fig_line.update_layout(template="plotly_white", hovermode="x unified")
        st.plotly_chart(fig_line, use_container_width=True)

    with tab2:
        st.subheader("Industry Peer Ranking (Avg Accrual Ratio)")
        rank_fig = px.bar(firm_summary.sort_values('Avg_Accrual_Ratio'), x='tic', y='Avg_Accrual_Ratio', 
                          color='Avg_Accrual_Ratio', color_continuous_scale='RdYlGn_r')
        
        # --- 优化后的基准线逻辑：更加清晰醒目 ---
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
        st.subheader("Dynamic Positioning within Sector")
        # 动态高亮逻辑
        df_plot = df.copy()
        df_plot['Status'] = df_plot['tic'].apply(lambda x: 'Selected Firm' if x == ticker else 'Industry Peers')
        
        fig_global = px.scatter(
            df_plot, x='Rev_Growth', y='Accrual_Ratio', 
            color='Status',
            color_discrete_map={'Selected Firm': '#FF4B4B', 'Industry Peers': '#003366'},
            hover_name='tic', size='at', template="plotly_white"
        )
        st.plotly_chart(fig_global, use_container_width=True)

    # --- Footer ---
    st.divider()
    with st.expander("🔬 Statistical Deep Dive & Methodology"):
        col_m, col_f = st.columns(2)
        with col_m:
            st.markdown("**Correlation Matrix**")
            st.write(data[['ni', 'oancf', 'Accrual_Ratio', 'Rev_Growth']].corr())
        with col_f:
            st.markdown("**Academic Methodology**")
            st.latex(r"Accrual Ratio = \frac{NI - OCF}{Avg Assets}")
            st.write("Sloan (1996) suggests that high accruals indicate potential future earnings reversal.")

st.caption("Financial Analysis Project | ACC102")