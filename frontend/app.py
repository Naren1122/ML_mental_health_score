import streamlit as st
import pandas as pd

from styles import load_css
from api_client import predict_single_model, predict_all_models
from components import (
    render_input_form,
    render_score_card,
    render_recommendations,
    render_correlation_heatmap
)

# 1. Page Configuration & Custom CSS Injection
st.set_page_config(
    page_title="MindScore • Student Mental Health Platform",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)
load_css()

# 2. Sidebar Navigation & Branding
st.sidebar.markdown("""
<div class="sidebar-brand">
    <span style="font-size: 1.8rem;">🧠</span>
    <div>
        <h2>MindScore AI</h2>
        <span class="api-status">● API Connected</span>
    </div>
</div>
""", unsafe_allow_html=True)

menu = st.sidebar.radio(
    "Select Destination:",
    [
        "🏠 Home & Overview",
        "🚀 XGBoost Regressor",
        "🌲 Random Forest Regressor",
        "📈 Linear Regression",
        "🎯 K-Nearest Neighbors (KNN)",
        "⚙️ Support Vector Regressor (SVR)",
        "⚖️ Compare All Models"
    ],
    index=0
)

MODEL_KEY_MAP = {
    "🚀 XGBoost Regressor": "xgboost",
    "🌲 Random Forest Regressor": "random_forest",
    "📈 Linear Regression": "linear_regression",
    "🎯 K-Nearest Neighbors (KNN)": "knn",
    "⚙️ Support Vector Regressor (SVR)": "svr"
}

# -------------------------------------------------------------
# 1. HOME & OVERVIEW
# -------------------------------------------------------------
if menu == "🏠 Home & Overview":
    st.markdown("""
    <div class="hero-banner">
        <h1 class="hero-title">Student Mental Health & Social Media Platform</h1>
        <p class="hero-subtitle">
            An intelligent machine learning assessment tool evaluating how digital screen habits, 
            sleep architecture, and academic routines shape student mental wellbeing.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 3 High-level Metric Highlights
    stat_col1, stat_col2, stat_col3 = st.columns(3)
    with stat_col1:
        st.markdown("""
        <div class="stat-tile">
            <div class="stat-val">+0.77</div>
            <div class="stat-label">Sleep Protection Factor</div>
            <p style="font-size: 0.8rem; color:#64748B; margin: 0.3rem 0 0 0;">Highest positive correlation with mental stability</p>
        </div>
        """, unsafe_allow_html=True)

    with stat_col2:
        st.markdown("""
        <div class="stat-tile">
            <div class="stat-val">-0.82</div>
            <div class="stat-label">Heavy Screen Time Drag</div>
            <p style="font-size: 0.8rem; color:#64748B; margin: 0.3rem 0 0 0;">Negative correlation when usage exceeds 6 hrs/day</p>
        </div>
        """, unsafe_allow_html=True)

    with stat_col3:
        st.markdown("""
        <div class="stat-tile">
            <div class="stat-val">5 Models</div>
            <div class="stat-label">ML Ensemble Suite</div>
            <p style="font-size: 0.8rem; color:#64748B; margin: 0.3rem 0 0 0;">XGBoost, Random Forest, SVR, KNN & Linear Regression</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    colA, colB = st.columns([1.4, 1])
    with colA:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-header">📖 Understanding the Mental Wellbeing Score</div>', unsafe_allow_html=True)
        st.markdown("""
        The **Mental Health Score** ranges from **1.0 (Critical Psychological Distress)** to **10.0 (High Resilience & Equilibrium)**.

        * 🟢 **8.0 – 10.0 (Resilient & Thriving):** Balanced screen time, consistent sleep (>7.5 hrs), and active lifestyle.
        * 🔵 **6.5 – 7.9 (Balanced & Healthy):** Moderate social media usage with adequate rest; minor academic stressors.
        * 🟠 **5.0 – 6.4 (Mild Distress):** High screen consumption (4.5–6 hrs) with compromised sleep (<6.5 hrs).
        * 🔴 **1.0 – 4.9 (High Distress / At Risk):** Chronic phone unlocks (>200/day) combined with sleep deprivation.
        """)
        st.info("👈 **Get started:** Choose any model from the sidebar to predict a score or compare all 5 algorithms side-by-side.")
        st.markdown('</div>', unsafe_allow_html=True)

    with colB:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-header">🤖 Deployed Regression Models</div>', unsafe_allow_html=True)
        st.markdown("""
        * **🚀 XGBoost Regressor:** Gradient-boosted decision trees tuned for subtle non-linear interactions.
        * **🌲 Random Forest:** Ensemble bagging regressor offering high stability against outliers.
        * **🎯 K-Nearest Neighbors (KNN):** Distance-based profiling clustering similar student lifestyles.
        * **⚙️ Support Vector Regressor (SVR):** Non-linear kernel capturing boundary relationships.
        * **📈 Linear Regression:** Parametric statistical baseline.
        """)
        st.markdown('</div>', unsafe_allow_html=True)

    # Heatmap on Home Overview
    render_correlation_heatmap()

# -------------------------------------------------------------
# 2. INDIVIDUAL MODEL DASHBOARD
# -------------------------------------------------------------
elif menu in MODEL_KEY_MAP:
    model_name = menu
    model_key = MODEL_KEY_MAP[menu]

    st.markdown(f"""
    <div style="margin-bottom: 1.5rem;">
        <h1 style="font-size: 2.2rem; font-weight: 800; color: #1E293B; margin: 0;">{model_name}</h1>
        <p style="color: #64748B; font-size: 1rem; margin-top: 0.2rem;">Adjust student attributes below to calculate the estimated mental wellbeing score in real-time.</p>
    </div>
    """, unsafe_allow_html=True)

    features = render_input_form()

    predict_btn = st.button("🔮 Calculate Mental Wellbeing Score", type="primary")

    if predict_btn:
        with st.spinner("Calling FastAPI inference service..."):
            pred = predict_single_model(model_key, features)
            if pred:
                st.markdown("<br>", unsafe_allow_html=True)
                col_left, col_right = st.columns([1, 1.4])
                with col_left:
                    render_score_card(pred["predicted_score"], pred["category"], pred["status_color"])
                with col_right:
                    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                    render_recommendations(pred["recommendations"])
                    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    render_correlation_heatmap()

# -------------------------------------------------------------
# 3. COMPARE ALL MODELS
# -------------------------------------------------------------
elif menu == "⚖️ Compare All Models":
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <h1 style="font-size: 2.2rem; font-weight: 800; color: #1E293B; margin: 0;">Multi-Model Benchmark Comparison</h1>
        <p style="color: #64748B; font-size: 1rem; margin-top: 0.2rem;">Simultaneously test the same student lifestyle profile across all 5 regression algorithms.</p>
    </div>
    """, unsafe_allow_html=True)

    features = render_input_form()

    if st.button("⚡ Run Multi-Model Comparison", type="primary"):
        with st.spinner("Querying all 5 algorithms via FastAPI..."):
            data = predict_all_models(features)
            if data:
                preds = data["predictions"]
                st.markdown("<br>", unsafe_allow_html=True)
                
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.markdown('<div class="card-header">📊 Model Output Comparison</div>', unsafe_allow_html=True)

                cols = st.columns(len(preds))
                for idx, (k, score) in enumerate(preds.items()):
                    with cols[idx]:
                        st.metric(
                            label=k.replace('_', ' ').title(), 
                            value=f"{score:.2f} / 10"
                        )

                st.markdown("<br>", unsafe_allow_html=True)
                chart_df = pd.DataFrame({
                    "Model": [k.replace('_', ' ').title() for k in preds.keys()],
                    "Predicted Wellbeing Score": list(preds.values())
                }).set_index("Model")
                
                st.bar_chart(chart_df)
                st.markdown('</div>', unsafe_allow_html=True)

                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                render_recommendations(data["recommendations"])
                st.markdown('</div>', unsafe_allow_html=True)
