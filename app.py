import streamlit as st
import json
import os
from datetime import date
import plotly.graph_objects as go

# =====================================================
# FILES
# =====================================================
ACH_FILE = "achievements.json"
STUDY_FILE = "study.json"

# =====================================================
# CREATE FILES IF NOT EXIST
# =====================================================
if not os.path.exists(ACH_FILE):
    with open(ACH_FILE, "w") as f:
        json.dump([], f)

if not os.path.exists(STUDY_FILE):
    with open(STUDY_FILE, "w") as f:
        json.dump([], f)

# =====================================================
# FUNCTIONS
# =====================================================
def load_data(file):
    try:
        with open(file, "r") as f:
            content = f.read().strip()
            if content == "":
                return []
            return json.loads(content)
    except:
        return []

def save_data(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

def calculate_xp():
    study_data = load_data(STUDY_FILE)
    achievements = load_data(ACH_FILE)
    
    # 100 XP per completed topic, 50 XP per achievement
    completed_topics = sum(1 for item in study_data if item.get("completed", False))
    total_xp = (completed_topics * 100) + (len(achievements) * 50)
    level = (total_xp // 500) + 1
    return total_xp, level

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="Shlok Study Tracker",
    page_icon="📚",
    layout="wide"
)

# =====================================================
# OP CUSTOM CSS (Kid Friendly & Gamified)
# =====================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka+One&family=Nunito:wght@400;700&display=swap');

    /* Global Font */
    html, body, [class*="css"] {
        font-family: 'Nunito', sans-serif;
    }
    
    h1, h2, h3 {
        font-family: 'Fredoka One', cursive !important;
    }

    /* Animated Header */
    .hero-title {
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4, #45B7D1, #FF6B6B);
        background-size: 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradient 5s ease infinite;
        text-align: center;
        font-size: 55px !important;
        margin-bottom: 10px;
    }

    @keyframes gradient {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }

    /* Style the Cards */
    div[data-testid="stVerticalBlock"] div[style*="border"] {
        border-radius: 20px !important;
        box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.1) !important;
        border: 3px solid #4ECDC4 !important;
        transition: transform 0.2s;
        background-color: rgba(255, 255, 255, 0.05);
    }
    
    div[data-testid="stVerticalBlock"] div[style*="border"]:hover {
        transform: translateY(-5px);
        border: 3px solid #FF6B6B !important;
    }

    /* Button Styling */
    div[data-testid="stButton"] button {
        border-radius: 15px;
        font-weight: bold;
        transition: 0.3s;
    }

    /* Player Stats Box */
    .stats-box {
        background: linear-gradient(135deg, #FFD93D, #FF6B6B);
        border-radius: 15px;
        padding: 15px;
        color: white;
        text-align: center;
        font-family: 'Fredoka One', cursive;
        margin-bottom: 20px;
        box-shadow: 0px 5px 10px rgba(0,0,0,0.2);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =====================================================
# NAVBAR & HEADER
# =====================================================
st.markdown('<h1 class="hero-title">📚 Shlok Study Tracker</h1>', unsafe_allow_html=True)

# Gamification Stats
total_xp, current_level = calculate_xp()
st.markdown(
    f"""
    <div class="stats-box">
        <h2>⭐ Level {current_level} Student</h2>
        <p style="font-size: 20px; margin:0;">Total XP: {total_xp} / {(current_level)*500}</p>
    </div>
    """, 
    unsafe_allow_html=True
)

# =====================================================
# NAVIGATION
# =====================================================
st.markdown("---")
menu = st.radio(
    "Navigation",
    ["📖 Study Planner", "🏆 Achievements"],
    horizontal=True
)
st.markdown("---")

# =====================================================
# STUDY PLANNER SECTION
# =====================================================
if menu == "📖 Study Planner":
    
    colA, colB = st.columns([2, 1])

    with colB:
        st.subheader("📊 Overall Progress")
        study_data = load_data(STUDY_FILE)
        
        total = len(study_data)
        completed_count = sum(1 for item in study_data if item.get("completed", False))
        percentage = int((completed_count / total * 100) if total > 0 else 0)

        # OP Visualization: Plotly Gauge Chart
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = percentage,
            number = {'suffix': "%", 'font': {'size': 50, 'color': "#4ECDC4"}},
            title = {'text': "Completion", 'font': {'size': 20}},
            gauge = {
                'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "white"},
                'bar': {'color': "#FF6B6B"},
                'bgcolor': "rgba(0,0,0,0)",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 33], 'color': "rgba(255, 107, 107, 0.2)"},
                    {'range': [33, 66], 'color': "rgba(255, 217, 61, 0.3)"},
                    {'range': [66, 100], 'color': "rgba(78, 205, 196, 0.4)"}],
                'threshold': {
                    'line': {'color': "#FFD93D", 'width': 4},
                    'thickness': 0.75,
                    'value': 100}
            }
        ))
        fig.update_layout(height=300, margin=dict(l=10, r=10, t=40, b=10), paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)
        
        st.write(f"**Completed Topics: {completed_count}/{total}**")

        if percentage == 100 and total > 0:
            st.success("🎉 All Topics Completed!")
            st.balloons()

        st.markdown("### ➕ Add Study Topic")
        with st.form("study_form", clear_on_submit=True):
            subject = st.text_input("Subject Name", placeholder="e.g. Science")
            topic = st.text_input("Subtopic / Chapter", placeholder="e.g. Gravity")
            submit = st.form_submit_button("Add Topic")
            
            if submit and subject and topic:
                study_data.append({"subject": subject, "topic": topic, "completed": False})
                save_data(STUDY_FILE, study_data)
                st.success("Topic Added Successfully!")
                st.rerun()

    with colA:
        st.subheader("📚 Preparation Tracking")
        if len(study_data) == 0:
            st.info("No study topics added yet.")
        else:
            updated_data = []
            has_changed = False  
            
            for i, item in enumerate(study_data):
                c1, c2, c3 = st.columns([0.5, 4, 0.5], gap="small")
                
                with c1:
                    st.write("") # Spacing
                    checked = st.checkbox("", value=item["completed"], key=f"check_{i}")
                
                with c2:
                    with st.container(border=True):
                        if checked:
                            st.markdown(f"### 🟢 ~~{item['subject']}~~")
                            st.caption(f"~~Topic: {item['topic']}~~")
                        else:
                            st.markdown(f"### 📘 {item['subject']}")
                            st.caption(f"**Topic:** {item['topic']}")
                
                with c3:
                    st.write("") # Spacing
                    delete = st.button("❌", key=f"delete_{i}")

                if delete:
                    has_changed = True
                    st.toast("Topic deleted.")
                else:
                    if item["completed"] != checked:
                        item["completed"] = checked
                        has_changed = True
                        if checked:
                            st.toast("Topic Completed! +100 XP! 🌟")
                    updated_data.append(item)

            if has_changed:
                save_data(STUDY_FILE, updated_data)
                st.rerun()

# =====================================================
# ACHIEVEMENTS SECTION
# =====================================================
elif menu == "🏆 Achievements":

    st.subheader("📌 All Achievements")
    
    achievements = load_data(ACH_FILE)
    
    if len(achievements) == 0:
        st.info("No achievements added yet.")
    else:
        cols = st.columns(3)
        updated_achievements = []
        has_changed = False
        
        for i, a in enumerate(achievements):
            col = cols[i % 3] 
            with col:
                with st.container(border=True):
                    st.markdown(f"## 🏅 {a['title']}")
                    st.markdown(f"**Category:** `{a['category']}`")
                    st.caption(f"📅 *Date: {a['date']}*")
                    
                    delete = st.button("Delete", key=f"ach_delete_{i}", use_container_width=True)
            
            if delete:
                has_changed = True
                st.toast("Achievement Deleted.")
            else:
                updated_achievements.append(a)

        if has_changed:
            save_data(ACH_FILE, updated_achievements)
            st.rerun()

    st.markdown("---")
    st.subheader("➕ Add Achievement")

    col1, col2 = st.columns(2)
    with col1:
        with st.form("achievement_form", clear_on_submit=True):
            title = st.text_input("Achievement Name")
            category = st.text_input("Category")
            ach_date = st.date_input("Achievement Date", value=date.today())
            submit = st.form_submit_button("Add Achievement")

        if submit and title and category:
            achievements.append({
                "title": title,
                "category": category,
                "date": str(ach_date)
            })
            save_data(ACH_FILE, achievements)
            st.success("Achievement Added Successfully! +50 XP! 🌟")
            st.snow()
            st.rerun()