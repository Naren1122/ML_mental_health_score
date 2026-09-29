import streamlit as st

CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Background & Container */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    /* Hero Banner */
    .hero-banner {
        background: linear-gradient(135deg, #1E1B4B 0%, #312E81 50%, #4338CA 100%);
        border-radius: 16px;
        padding: 2.2rem 2.5rem;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px -5px rgba(67, 56, 202, 0.25);
    }
    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        margin: 0 0 0.5rem 0;
        color: #FFFFFF;
    }
    .hero-subtitle {
        font-size: 1.05rem;
        color: #C7D2FE;
        margin: 0;
        line-height: 1.5;
        max-width: 750px;
    }

    /* Section Cards */
    .glass-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.04), 0 2px 4px -2px rgba(0, 0, 0, 0.02);
        margin-bottom: 1.5rem;
    }
    .card-header {
        font-size: 1.1rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* Score Card Hero */
    .score-hero-card {
        background: linear-gradient(180deg, #FFFFFF 0%, #F8FAFC 100%);
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 2rem 1.5rem;
        text-align: center;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
    }
    .score-number {
        font-size: 3.8rem;
        font-weight: 800;
        line-height: 1;
        margin: 0.8rem 0;
        letter-spacing: -0.03em;
    }
    .score-badge {
        display: inline-block;
        padding: 0.4rem 1.2rem;
        border-radius: 9999px;
        font-weight: 700;
        font-size: 0.9rem;
        letter-spacing: 0.01em;
    }

    /* Recommendations Box */
    .rec-item {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-left: 4px solid #6366F1;
        border-radius: 8px;
        padding: 0.9rem 1.1rem;
        margin-bottom: 0.7rem;
        font-size: 0.92rem;
        color: #334155;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.03);
    }

    /* Stat Highlight Tile */
    .stat-tile {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
    }
    .stat-val {
        font-size: 1.8rem;
        font-weight: 800;
        color: #4F46E5;
    }
    .stat-label {
        font-size: 0.85rem;
        color: #64748B;
        font-weight: 600;
        margin-top: 0.2rem;
    }

    /* Streamlit Primary Button Override */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #4F46E5 0%, #4338CA 100%);
        color: white;
        font-weight: 600;
        font-size: 1rem;
        padding: 0.65rem 2rem;
        border-radius: 10px;
        border: none;
        width: 100%;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
        transition: all 0.2s ease-in-out;
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 16px rgba(79, 70, 229, 0.4);
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #F8FAFC;
        border-right: 1px solid #E2E8F0;
    }
    .sidebar-brand {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        padding: 0.5rem 0 1.2rem 0;
        border-bottom: 1px solid #E2E8F0;
        margin-bottom: 1rem;
    }
    .sidebar-brand h2 {
        font-size: 1.25rem;
        font-weight: 800;
        color: #1E293B;
        margin: 0;
    }
    .api-status {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        background: #DCFCE7;
        color: #15803D;
        font-size: 0.75rem;
        font-weight: 700;
        padding: 0.2rem 0.6rem;
        border-radius: 9999px;
    }
</style>
"""

def load_css():
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
