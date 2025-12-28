import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import scipy.stats as scs
import requests
import time
import math
from statsmodels.stats.power import NormalIndPower
from streamlit_lottie import st_lottie
from src.experiment import ABTestEngine

# --- 1. APP CONFIGURATION ---
st.set_page_config(
    page_title="OptiFlow Enterprise | A/B Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. ASSET LOADING ---
@st.cache_data
def load_lottie(url):
    try:
        r = requests.get(url, timeout=2)
        return r.json() if r.status_code == 200 else None
    except:
        return None

lottie_success = load_lottie("https://assets10.lottiefiles.com/packages/lf20_lk80fpsm.json")
lottie_stats = load_lottie("https://assets3.lottiefiles.com/packages/lf20_49rdyysj.json")

# --- 3. DYNAMIC STYLING (Based on user choice) ---
# We will inject CSS dynamically later in the script based on sidebar inputs

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown("### ⚡ OptiFlow Pro")
    
    with st.expander("🛠️ Experiment Setup", expanded=True):
        n_users = st.slider("Traffic Volume (Users)", 5000, 100000, 20000, step=1000)
        baseline = st.slider("Baseline Conversion Rate", 0.05, 0.40, 0.12, 0.01)
        lift = st.slider("Target Lift (Impact)", 0.005, 0.05, 0.02, 0.005)
    
    with st.expander("⚙️ Statistical Precision"):
        alpha = st.select_slider("Significance Level", options=[0.10, 0.05, 0.01], value=0.05)
        simulations = st.slider("Monte Carlo Iterations", 10, 100, 20)

    # --- NEW CUSTOMIZATION SECTION ---
    with st.expander("🎨 Interface Customization", expanded=False):
        st.markdown("**Visuals**")
        brand_color = st.color_picker("Brand Accent Color", "#2563eb") # Default Blue
        chart_theme = st.selectbox("Chart Theme", ["plotly_white", "plotly_dark", "ggplot2", "seaborn"])
        
        st.markdown("**Interaction**")
        enable_confetti = st.checkbox("Enable Celebrations", value=True)
        show_raw_data = st.checkbox("Show Raw Data Table", value=False)

    st.markdown("---")
    run_btn = st.button("🚀 Run Simulation", type="primary", use_container_width=True)

# --- INJECT CSS ---
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700&display=swap');
    html, body, [class*="css"] {{ font-family: 'Plus Jakarta Sans', sans-serif; }}
    
    .kpi-card {{
        background: linear-gradient(145deg, #ffffff, #f0f2f6);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        border: 1px solid #ffffff;
        transition: all 0.3s ease;
    }}
    .kpi-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.12);
    }}
    .kpi-title {{ font-size: 14px; color: #64748b; font-weight: 600; letter-spacing: 0.5px; text-transform: uppercase; }}
    .kpi-value {{ font-size: 32px; color: #0f172a; font-weight: 700; margin: 8px 0; }}
    .kpi-sub {{ font-size: 13px; color: #94a3b8; }}
    .badge-success {{ background-color: {brand_color}20; color: {brand_color}; padding: 4px 12px; border-radius: 20px; font-weight: 600; font-size: 12px; }}
    
    /* Customize Streamlit Elements to match brand */
    div.stButton > button:first-child {{
        background-color: {brand_color};
        color: white;
    }}
    
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
</style>
""", unsafe_allow_html=True)

# --- 5. EXECUTION LOGIC ---
if 'results' not in st.session_state:
    st.session_state.results = None

if run_btn:
    with st.spinner("Initializing Experiment Engine..."):
        # Fake loader for UX
        progress_bar = st.progress(0)
        for i in range(50):
            time.sleep(0.01)
            progress_bar.progress(i * 2)
        
        engine = ABTestEngine(baseline_rate=baseline, lift=lift, sample_size=n_users)
        engine.run_simulation()
        
        st.session_state.results = {
            'stats': engine.get_statistics(),
            'trend': engine.get_trend_data(),
            'engine': engine
        }
        progress_bar.empty()

# --- 6. MAIN DASHBOARD ---
if st.session_state.results:
    data = st.session_state.results
    stats = data['stats']
    
    # Header
    c1, c2 = st.columns([3, 1])
    with c1:
        st.title("Experiment Results Dashboard")
        st.markdown(f"**Status:** Analysis Complete | **Sample Size:** {n_users:,} Users")
    with c2:
        # Only show confetti if enabled AND result is significant
        if stats['p_value'] < alpha and lottie_success and enable_confetti:
            st_lottie(lottie_success, height=100, key="success")
    
    st.markdown("---")

    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    control_rate = stats['control_rate']
    test_rate = stats['test_rate']
    actual_lift = stats['lift']
    is_sig = stats['p_value'] < alpha
    
    with col1:
        st.markdown(f"""<div class="kpi-card"><div class="kpi-title">Control</div><div class="kpi-value">{control_rate:.2%}</div><div class="kpi-sub">Baseline</div></div>""", unsafe_allow_html=True)
    with col2:
        # Use Brand Color for lift Badge
        st.markdown(f"""<div class="kpi-card"><div class="kpi-title">Test</div><div class="kpi-value">{test_rate:.2%}</div><div class="badge-success">{actual_lift:+.2%} Lift</div></div>""", unsafe_allow_html=True)
    with col3:
        p_color = brand_color if is_sig else "#ca8a04"
        st.markdown(f"""<div class="kpi-card"><div class="kpi-title">P-Value</div><div class="kpi-value" style="color:{p_color}">{stats['p_value']:.4f}</div><div class="kpi-sub">Alpha: {alpha}</div></div>""", unsafe_allow_html=True)
    with col4:
        dec = "LAUNCH 🚀" if (is_sig and actual_lift > 0) else "WAIT 🛑"
        txt_col = brand_color if "LAUNCH" in dec else "#991b1b"
        st.markdown(f"""<div class="kpi-card" style="border:2px solid {txt_col}"><div class="kpi-title">Decision</div><div class="kpi-value" style="color:{txt_col};font-size:24px">{dec}</div><div class="kpi-sub">Recommendation</div></div>""", unsafe_allow_html=True)

    st.markdown("###")

    # TABS
    tab1, tab2, tab3 = st.tabs(["🔮 Monte Carlo", "📊 Distribution", "⚡ Power Analysis"])

    with tab1:
        st.markdown("##### 50 Simulations of Future Performance")
        fig_mc = go.Figure()
        dates = pd.date_range(start="2024-01-01", periods=30)
        
        # Ghost lines use brand color with low opacity
        # Convert hex to rgba for opacity
        brand_hex = brand_color.lstrip('#')
        brand_rgb = tuple(int(brand_hex[i:i+2], 16) for i in (0, 2, 4))
        ghost_color = f"rgba({brand_rgb[0]}, {brand_rgb[1]}, {brand_rgb[2]}, 0.1)"
        
        for _ in range(simulations):
            noise = np.random.normal(0, 0.005, 30)
            sim_trend = np.linspace(test_rate - 0.01, test_rate + 0.005, 30) + noise
            fig_mc.add_trace(go.Scatter(x=dates, y=sim_trend, mode='lines', line=dict(color=ghost_color, width=1), hoverinfo='skip'))
        
        fig_mc.add_trace(go.Scatter(x=dates, y=[control_rate]*30, mode='lines', name='Control', line=dict(color='#64748b', dash='dash', width=2)))
        fig_mc.add_trace(go.Scatter(x=dates, y=np.linspace(test_rate - 0.01, test_rate, 30), mode='lines', name='Test', line=dict(color=brand_color, width=4)))
        
        fig_mc.update_layout(template=chart_theme, showlegend=False, height=400, yaxis_tickformat=".1%", margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig_mc, use_container_width=True)

    with tab2:
        c_d1, c_d2 = st.columns([2, 1])
        with c_d1:
            st.markdown("##### Bayesian Posterior Distributions")
            x = np.linspace(min(control_rate, test_rate) - 0.04, max(control_rate, test_rate) + 0.04, 1000)
            y_c = scs.norm.pdf(x, control_rate, np.sqrt(control_rate*(1-control_rate)/(n_users/2)))
            y_t = scs.norm.pdf(x, test_rate, np.sqrt(test_rate*(1-test_rate)/(n_users/2)))
            fig_dist = go.Figure()
            fig_dist.add_trace(go.Scatter(x=x, y=y_c, fill='tozeroy', name='Control', line_color='#94a3b8'))
            fig_dist.add_trace(go.Scatter(x=x, y=y_t, fill='tozeroy', name='Test', line_color=brand_color))
            fig_dist.update_layout(template=chart_theme, yaxis_visible=False, height=350, margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(fig_dist, use_container_width=True)
        with c_d2:
            st.markdown("##### Confidence Gauge")
            fig_g = go.Figure(go.Indicator(mode="gauge+number", value=(1-stats['p_value'])*100, title={'text':"Confidence %"}, gauge={'axis':{'range':[0,100]}, 'bar':{'color':"#0f172a"}, 'steps':[{'range':[0,(1-alpha)*100], 'color':"#f1f5f9"}, {'range':[(1-alpha)*100, 100], 'color':brand_color}], 'threshold':{'line':{'color':"#ef4444", 'width':4}, 'thickness':0.75, 'value':(1-alpha)*100}}))
            fig_g.update_layout(height=300, margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(fig_g, use_container_width=True)

    with tab3:
        st.markdown("##### Statistical Power Curve")
        try:
            p1 = max(0.001, min(0.999, test_rate))
            p2 = max(0.001, min(0.999, control_rate))
            
            if abs(p1 - p2) < 0.0001:
                st.warning("⚠️ The difference between groups is too small to calculate a reliable power curve.")
                h = 0.001 
            else:
                h = 2 * (math.asin(math.sqrt(p1)) - math.asin(math.sqrt(p2)))
                h = abs(h)

            analysis = NormalIndPower()
            x_axis = np.linspace(500, n_users * 1.5, 20)
            y_axis = []
            
            for n in x_axis:
                try:
                    power_val = analysis.solve_power(effect_size=h, nobs1=n/2, alpha=alpha, ratio=1.0)
                    y_axis.append(power_val)
                except:
                    y_axis.append(0)

            try:
                current_power = analysis.solve_power(effect_size=h, nobs1=n_users/2, alpha=alpha, ratio=1.0)
            except:
                current_power = 0

            fig_power = go.Figure()
            fig_power.add_trace(go.Scatter(x=x_axis, y=y_axis, mode='lines', name='Power Curve', line=dict(color=brand_color, width=4)))
            fig_power.add_trace(go.Scatter(x=[n_users], y=[current_power], mode='markers', name='Current Traffic', marker=dict(size=15, color='#ef4444', symbol='diamond', line=dict(width=2, color='white')), text=[f"Current Power: {current_power:.1%}"], hoverinfo='text'))
            fig_power.add_hline(y=0.8, line_dash="dot", line_color="#cbd5e1", annotation_text="Target (80%)")

            fig_power.update_layout(template=chart_theme, xaxis_title="Total Sample Size", yaxis_title="Statistical Power (0-1)", yaxis_range=[0, 1.1], height=400, margin=dict(l=20, r=20, t=20, b=20), hovermode="x unified")
            st.plotly_chart(fig_power, use_container_width=True)
            
            if current_power < 0.8:
                try:
                    req_sample = analysis.solve_power(effect_size=h, power=0.8, alpha=alpha, ratio=1.0) * 2
                    st.error(f"⚠️ **Low Power:** You only have {current_power:.1%} power. To reach 80%, you need ~{int(req_sample):,} total users.")
                except:
                    st.info("Low power detected.")
            else:
                st.success(f"✅ **High Power:** You have {current_power:.1%} power. Your sample size is sufficient!")

        except Exception as e:
            st.error(f"Could not render Power Analysis: {str(e)}")

    # RAW DATA TOGGLE
    if show_raw_data:
        st.markdown("### 🗃️ Raw Data View")
        st.dataframe(data['trend'])

else:
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        if lottie_stats:
            st_lottie(lottie_stats, height=300)
        st.markdown("""<div style="text-align: center;"><h2>Ready to Optimize?</h2><p style="color: #64748b;">Configure sidebar & click <b>Run Simulation</b>.</p></div>""", unsafe_allow_html=True)