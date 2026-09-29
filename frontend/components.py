import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def render_input_form() -> dict:
    """Renders organized input sections for student demographics, screen time, and wellness."""
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="card-header">🎓 Demographics & Studies</div>', unsafe_allow_html=True)
        age = st.slider("Age", 16, 30, 21, help="Age of the student")
        gender = st.selectbox("Gender", ["Female", "Male"])
        country = st.selectbox("Country", [
            "USA", "India", "Canada", "Australia", "UK", 
            "Germany", "Mexico", "Turkey", "France", "Other"
        ])
        academic_level = st.selectbox("Academic Level", ["Undergraduate", "Graduate", "High School"])
        study_hours = st.slider("Daily Study Hours", 0.0, 12.0, 4.0, step=0.5)

    with col2:
        st.markdown('<div class="card-header">📱 Digital & Social Media</div>', unsafe_allow_html=True)
        platform = st.selectbox("Most Used Platform", [
            "Instagram", "TikTok", "YouTube", "Facebook", "Snapchat", 
            "Twitter", "WhatsApp", "LinkedIn", "WeChat", "LINE", "KakaoTalk", "VKontakte"
        ])
        purpose = st.selectbox("Primary Purpose of Use", ["Entertainment", "Education", "Networking", "News"])
        daily_usage = st.slider("Daily Screen Time (Hours)", 0.0, 14.0, 4.5, step=0.5)
        daily_unlocks = st.slider("Daily Phone Unlocks", 10, 350, 120, step=5)

    with col3:
        st.markdown('<div class="card-header">🌙 Health & Rest</div>', unsafe_allow_html=True)
        sleep_hours = st.slider("Sleep Hours Per Night", 3.0, 12.0, 7.0, step=0.5)
        physical_activity = st.slider("Exercise (Hours/Day)", 0.0, 6.0, 1.5, step=0.5)
        stress_level = st.select_slider(
            "Self-Reported Stress Level", 
            options=["Low", "Medium", "High", "Very High"], 
            value="Medium"
        )
        st.markdown("<br>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    return {
        "Age": age,
        "Gender": gender,
        "Country": country,
        "Academic_Level": academic_level,
        "Most_Used_Platform": platform,
        "Purpose_Of_Use": purpose,
        "Avg_Daily_Usage_Hours": daily_usage,
        "Daily_Unlocks": daily_unlocks,
        "Study_Hours": study_hours,
        "Physical_Activity_Hours": physical_activity,
        "Sleep_Hours_Per_Night": sleep_hours,
        "Stress_Level": stress_level
    }

def render_score_card(score: float, category: str, color: str):
    """Renders a sleek, elevated score indicator with dynamic color coding."""
    st.markdown(f"""
    <div class="score-hero-card">
        <span style="font-size: 0.85rem; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em;">
            Predicted Mental Wellbeing Score
        </span>
        <div class="score-number" style="color: {color};">
            {score}<span style="font-size: 1.6rem; color: #94A3B8; font-weight: 500;"> / 10</span>
        </div>
        <span class="score-badge" style="background-color: {color}1A; color: {color}; border: 1.5px solid {color};">
            ● {category}
        </span>
    </div>
    """, unsafe_allow_html=True)

    # Clean progress bar
    normalized = min(max((score - 1.0) / 9.0, 0.0), 1.0)
    st.progress(normalized)

def render_recommendations(recs: list):
    """Renders actionable lifestyle insights in structured cards."""
    st.markdown('<div class="card-header">💡 Personalized Lifestyle Insights</div>', unsafe_allow_html=True)
    for r in recs:
        st.markdown(f'<div class="rec-item">{r}</div>', unsafe_allow_html=True)

@st.cache_data
def get_correlation_matrix():
    """Reads dataset once and calculates correlation for key features."""
    df = pd.read_csv('Student Social Media And Mental Health Impact.csv')
    cols = {
        'Avg_Daily_Usage_Hours': 'Screen Time',
        'Daily_Unlocks': 'Phone Unlocks',
        'Sleep_Hours_Per_Night': 'Sleep',
        'Physical_Activity_Hours': 'Exercise',
        'Study_Hours': 'Study',
        'Age': 'Age',
        'Mental_Health_Score': 'Score'
    }
    return df[list(cols.keys())].rename(columns=cols).corr()

def render_correlation_heatmap():
    """Renders a compact, balanced heatmap framed by data insights."""
    corr = get_correlation_matrix()

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-header">🔥 Feature Correlation Matrix & Insights</div>', unsafe_allow_html=True)

    col_plot, col_insights = st.columns([1.1, 0.9])

    with col_plot:
        fig, ax = plt.subplots(figsize=(4.6, 3.6), dpi=110)
        fig.patch.set_facecolor('#FFFFFF')
        ax.set_facecolor('#FFFFFF')

        sns.heatmap(
            corr,
            annot=True,
            fmt=".2f",
            cmap="vlag",
            center=0,
            square=True,
            linewidths=0.6,
            linecolor='#FFFFFF',
            annot_kws={"size": 7.5, "weight": "bold"},
            cbar_kws={"shrink": 0.7, "aspect": 12},
            ax=ax
        )
        plt.xticks(rotation=28, ha='right', fontsize=7.5, color='#334155')
        plt.yticks(rotation=0, fontsize=7.5, color='#334155')
        plt.tight_layout()
        st.pyplot(fig, use_container_width=False)

    with col_insights:
        st.markdown("""
        **What does this correlation matrix tell us?**
        
        * 🌙 **Sleep (+0.77):** Highest positive correlation with Mental Health Score. Consistent restorative rest directly shields cognitive stability.
        * 📱 **Screen Time (-0.82):** Strongest negative factor. Heavy daily social media consumption correlates heavily with distress.
        * 🔓 **Phone Unlocks (+0.96 with Screen Time):** Frequent unlocking fragments focus and heightens baseline anxiety.
        * 🏃 **Physical Exercise (+0.52):** Moderate activity serves as a proven psychological stabilizer.
        """)

    st.markdown('</div>', unsafe_allow_html=True)
