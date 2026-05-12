import streamlit as st
import json
import os
from datetime import date
import plotly.graph_objects as go

# =====================================================
# DATA MANAGEMENT
# =====================================================
ACH_FILE = "achievements.json"
STUDY_FILE = "study.json"

def load_data(file):
    try:
        with open(file, "r") as f:
            content = f.read().strip()
            return json.loads(content) if content else []
    except: return []

def save_data(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

def calculate_xp():
    study_data = load_data(STUDY_FILE)
    achievements = load_data(ACH_FILE)
    completed_topics = sum(1 for item in study_data if item.get("completed", False))
    total_xp = (completed_topics * 100) + (len(achievements) * 50)
    level = (total_xp // 500) + 1
    return total_xp, level

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(page_title="Shlok Study Tracker", page_icon="📚", layout="wide")

if 'current_page' not in st.session_state:
    st.session_state['current_page'] = "📖 Study Planner"
    
# DEFAULT TO DARK MODE
if 'dark_mode' not in st.session_state:
    st.session_state['dark_mode'] = True 

# =====================================================
# THEME VARIABLES & CSS (MOBILE RESPONSIVE!)
# =====================================================
if st.session_state['dark_mode']:
    # Soft Grayish-Dark Theme
    bg_color = "#1E2227"
    text_color = "#E2E8F0"
    card_bg = "#282C34"
    card_border = "#3E4451"
    input_bg = "#282C34"
    gauge_bg = "#282C34"
    gauge_font = "#818CF8"
    gauge_tick = "#475569"
else:
    # Crisp Light Theme
    bg_color = "#F8FAFC"
    text_color = "#1E293B"
    card_bg = "#FFFFFF"
    card_border = "#E2E8F0"
    input_bg = "#FFFFFF"
    gauge_bg = "#F1F5F9"
    gauge_font = "#6366F1"
    gauge_tick = "#CBD5E1"

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Fredoka:wght@500;600&display=swap');

    /* Main App Background */
    .stApp {{
        background-color: {bg_color}; 
        color: {text_color};
        font-family: 'Inter', sans-serif;
        transition: all 0.3s ease;
    }}

    h1, h2, h3, h4, p, span, label {{
        color: {text_color} !important;
    }}

    h1, h2, h3 {{
        font-family: 'Fredoka', sans-serif !important;
    }}

    /* Main Title */
    .hero-title {{
        text-align: center;
        color: #6366F1 !important;
        font-size: 42px !important;
        margin-bottom: 10px;
    }}

    /* OP DYNAMIC ANIMATED GRADIENT FOR LEVEL UP BANNER */
    .stats-box {{
        background: linear-gradient(-45deg, #8B5CF6, #3B82F6, #EC4899, #8B5CF6);
        background-size: 300% 300%;
        animation: gradientBg 6s ease infinite;
        border-radius: 20px;
        padding: 25px;
        color: white !important;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0px 10px 25px rgba(99, 102, 241, 0.25);
    }}
    .stats-box h2, .stats-box p {{
        color: white !important;
    }}

    @keyframes gradientBg {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}

    /* Section Cards */
    div[data-testid="stVerticalBlock"] div[style*="border"] {{
        background-color: {card_bg} !important;
        border: 1px solid {card_border} !important;
        border-radius: 16px !important;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.03) !important;
        transition: all 0.3s ease;
    }}

    /* Input Fields */
    div[data-baseweb="input"] > div {{
        background-color: {input_bg} !important;
        border: 2px solid {card_border} !important;
        border-radius: 10px !important;
    }}
    input {{
        color: {text_color} !important;
        font-weight: 500;
    }}
    
    /* Form Container */
    [data-testid="stForm"] {{
        background-color: {card_bg} !important;
        border: 1px solid {card_border} !important;
        border-radius: 16px !important;
        padding: 25px !important;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.03) !important;
    }}

    /* Tabs/Buttons */
    button[kind="primary"] {{
        background: linear-gradient(135deg, #6366F1, #8B5CF6) !important;
        border: none !important;
        color: white !important;
        border-radius: 12px !important;
        height: 3.5em !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        transition: 0.2s;
    }}
    
    button[kind="secondary"] {{
        background-color: {card_border} !important;
        color: {text_color} !important;
        border: none !important;
        border-radius: 12px !important;
        height: 3.5em !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        transition: 0.2s;
    }}

    .stCheckbox > label {{
        font-weight: 600;
    }}

    /* =========================================
       📱 MOBILE RESPONSIVENESS ADAPTATIONS 
       ========================================= */
    @media (max-width: 768px) {{
        .hero-title {{
            font-size: 32px !important; /* Smaller title on mobile */
        }}
        .stats-box {{
            padding: 15px !important; /* Tighter padding */
            border-radius: 15px !important;
            margin-bottom: 15px !important;
        }}
        .stats-box h2 {{
            font-size: 24px !important;
        }}
        .stats-box p {{
            font-size: 14px !important;
        }}
        button[kind="primary"], button[kind="secondary"] {{
            font-size: 14px !important; /* Smaller buttons */
            height: 3em !important;
            padding: 5px !important;
        }}
        [data-testid="stForm"] {{
            padding: 15px !important;
        }}
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# =====================================================
# HEADER & THEME TOGGLE
# =====================================================
col_title, col_toggle = st.columns([4, 1])
with col_title:
    st.markdown('<h1 class="hero-title">Shlok Study Tracker</h1>', unsafe_allow_html=True)
with col_toggle:
    st.write("") # Spacing
    theme_label = "☀️ Light" if not st.session_state['dark_mode'] else "🌙 Dark"
    if st.toggle(theme_label, value=st.session_state['dark_mode']):
        if not st.session_state['dark_mode']:
            st.session_state['dark_mode'] = True
            st.rerun()
    else:
        if st.session_state['dark_mode']:
            st.session_state['dark_mode'] = False
            st.rerun()

total_xp, current_level = calculate_xp()
st.markdown(
    f"""
    <div class="stats-box">
        <h2 style="margin:0;">⭐ Level {current_level} Student</h2>
        <p style="font-size: 18px; font-weight: 600; margin-top:5px; margin-bottom:0;">XP: {total_xp} / {(current_level)*500}</p>
    </div>
    """, 
    unsafe_allow_html=True
)

# =====================================================
# NAVIGATION
# =====================================================
col_nav1, col_nav2 = st.columns(2)
with col_nav1:
    btn_state1 = "primary" if st.session_state['current_page'] == "📖 Study Planner" else "secondary"
    if st.button("📖 Study Planner", use_container_width=True, type=btn_state1):
        st.session_state['current_page'] = "📖 Study Planner"
        st.rerun()

with col_nav2:
    btn_state2 = "primary" if st.session_state['current_page'] == "🏆 Achievements" else "secondary"
    if st.button("🏆 Achievements", use_container_width=True, type=btn_state2):
        st.session_state['current_page'] = "🏆 Achievements"
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)
menu = st.session_state['current_page']

# =====================================================
# STUDY PLANNER
# =====================================================
if menu == "📖 Study Planner":
    study_data = load_data(STUDY_FILE)
    
    # Using Streamlit's native column stacking for mobile
    col_main, col_side = st.columns([2.2, 1], gap="large")

    with col_main:
        st.markdown("### 📝 Preparation Tracking")
        if not study_data:
            st.info("You have no active missions. Add one to begin!")
        else:
            updated_data = []
            has_changes = False
            
            for i, item in enumerate(study_data):
                col_chk, col_card, col_btn = st.columns([0.3, 5, 0.5])
                with col_chk:
                    st.write("") 
                    is_done = st.checkbox("", value=item["completed"], key=f"t_{i}")
                with col_card:
                    with st.container(border=True):
                        if is_done:
                            st.markdown(f"**{item['subject']}** <span style='color:#10B981;'>(Done ✅)</span>", unsafe_allow_html=True)
                            st.caption(f"~~Topic: {item['topic']}~~")
                        else:
                            st.markdown(f"**{item['subject']}**")
                            st.caption(f"Topic: {item['topic']}")
                with col_btn:
                    st.write("") 
                    if st.button("🗑️", key=f"del_{i}"):
                        has_changes = True
                        continue
                
                if is_done != item["completed"]:
                    item["completed"] = is_done
                    has_changes = True
                updated_data.append(item)

            if has_changes:
                save_data(STUDY_FILE, updated_data)
                st.rerun()

    with col_side:
        st.markdown("### 📊 Progress")
        total = len(study_data)
        done = sum(1 for x in study_data if x["completed"])
        perc = int((done/total*100) if total > 0 else 0)

        # Theme-aware Plotly Gauge
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = perc,
            number = {'suffix': "%", 'font': {'color': gauge_font}},
            gauge = {
                'axis': {'range': [0, 100], 'tickcolor': gauge_tick},
                'bar': {'color': "#6366F1"},
                'bgcolor': gauge_bg,
                'borderwidth': 0
            }
        ))
        fig.update_layout(height=230, margin=dict(t=0, b=0, l=10, r=10), paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)

        # BALLOONS EFFECT ON 100% COMPLETION
        if perc == 100 and total > 0:
            st.balloons()
            st.success("🎉 All Missions Completed! You're unstoppable!")

        with st.form("new_task_form", clear_on_submit=True):
            st.markdown("#### Add New Mission")
            sub = st.text_input("Subject", placeholder="e.g. Science")
            top = st.text_input("Topic", placeholder="e.g. Gravity")
            if st.form_submit_button("Add to List", use_container_width=True):
                if sub and top:
                    study_data.append({"subject": sub, "topic": top, "completed": False})
                    save_data(STUDY_FILE, study_data)
                    st.rerun()

# =====================================================
# ACHIEVEMENTS
# =====================================================
else:
    ach_data = load_data(ACH_FILE)
    st.markdown("### 🏆 Your Trophy Room")
    
    if ach_data:
        # Columns will naturally wrap on smaller screens in Streamlit
        cols = st.columns(3)
        for idx, a in enumerate(ach_data):
            with cols[idx % 3]:
                with st.container(border=True):
                    st.markdown(f"#### 🏅 {a['title']}")
                    st.caption(f"**Category:** {a['category']}")
                    if st.button("Remove", key=f"adel_{idx}", use_container_width=True):
                        ach_data.pop(idx)
                        save_data(ACH_FILE, ach_data)
                        st.rerun()
    else:
        st.info("No achievements yet. Keep studying to earn XP and level up!")

    st.markdown("---")
    with st.form("new_ach_form", clear_on_submit=True):
        st.markdown("#### Claim a Trophy")
        # Ensure form inputs stack properly on mobile
        col1, col2 = st.columns(2)
        with col1:
            title = st.text_input("What did you achieve?")
        with col2:
            cat = st.text_input("Category (e.g. Exam, Sports)")
        
        if st.form_submit_button("Add to Wall of Fame", use_container_width=True):
            if title and cat:
                ach_data.append({"title": title, "category": cat, "date": str(date.today())})
                save_data(ACH_FILE, ach_data)
                st.balloons()
                st.rerun()