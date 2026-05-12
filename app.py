# Complete Streamlit Study Tracker App (Dynamic Version)

## app.py

import streamlit as st
import json
import os
from datetime import date

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

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Shlok Tracker",
    layout="wide"
)

# =====================================================
# TITLE
# =====================================================

st.title("📚 Shlok Achievement & Study Tracker")

# =====================================================
# SIDEBAR MENU
# =====================================================

menu = st.sidebar.radio(
    "Select Section",
    ["Achievements", "Study Planner"]
)

# =====================================================
# ACHIEVEMENTS SECTION
# =====================================================

if menu == "Achievements":

    st.header("🏆 Achievement Section")

    with st.form("achievement_form"):

        title = st.text_input("Achievement Name")

        category = st.text_input("Category")

        ach_date = st.date_input(
            "Achievement Date",
            value=date.today()
        )

        submit = st.form_submit_button("Add Achievement")

    if submit:

        if title and category:

            achievements = load_data(ACH_FILE)

            achievements.append({
                "title": title,
                "category": category,
                "date": str(ach_date)
            })

            save_data(ACH_FILE, achievements)

            st.success("Achievement Added Successfully!")

    st.subheader("📌 All Achievements")

    achievements = load_data(ACH_FILE)

    if len(achievements) == 0:

        st.info("No achievements added yet.")

    else:

        updated_achievements = []

        for i, a in enumerate(achievements):

            col1, col2 = st.columns([6, 1])

            with col1:

                with st.container(border=True):

                    st.markdown(f"### 🏅 {a['title']}")
                    st.write(f"Category: {a['category']}")
                    st.write(f"Date: {a['date']}")

            with col2:

                delete = st.button(
                    "❌",
                    key=f"ach_delete_{i}"
                )

            if not delete:
                updated_achievements.append(a)

        save_data(ACH_FILE, updated_achievements)

# =====================================================
# STUDY PLANNER SECTION
# =====================================================

elif menu == "Study Planner":

    st.header("📖 Study Planner")

    # ---------------- ADD TOPIC ----------------

    with st.form("study_form"):

        subject = st.text_input("Subject Name")

        topic = st.text_input("Subtopic / Chapter")

        submit = st.form_submit_button("Add Topic")

    if submit:

        if subject and topic:

            study_data = load_data(STUDY_FILE)

            study_data.append({
                "subject": subject,
                "topic": topic,
                "completed": False
            })

            save_data(STUDY_FILE, study_data)

            st.success("Topic Added Successfully!")

    # ---------------- SHOW TOPICS ----------------

    study_data = load_data(STUDY_FILE)

    st.subheader("📚 Preparation Tracking")

    if len(study_data) == 0:

        st.info("No study topics added yet.")

    else:

        completed_count = 0

        updated_data = []

        for i, item in enumerate(study_data):

            col1, col2, col3 = st.columns([1, 5, 1])

            # ---------------- CHECKBOX ----------------

            with col1:

                checked = st.checkbox(
                    "",
                    value=item["completed"],
                    key=f"check_{i}"
                )

            # ---------------- TOPIC INFO ----------------

            with col2:

                with st.container(border=True):

                    st.markdown(
                        f"""
                        ### 📘 {item['subject']}

                        Topic: {item['topic']}
                        """
                    )

            # ---------------- DELETE BUTTON ----------------

            with col3:

                delete = st.button(
                    "❌",
                    key=f"delete_{i}"
                )

            # ---------------- DELETE LOGIC ----------------

            if not delete:

                item["completed"] = checked

                updated_data.append(item)

                if checked:
                    completed_count += 1

        # ---------------- SAVE UPDATED DATA ----------------

        save_data(STUDY_FILE, updated_data)

        # ---------------- PROGRESS ----------------

        total = len(updated_data)

        progress = completed_count / total if total > 0 else 0

        st.subheader("📊 Overall Progress")

        st.progress(progress)

        st.write(f"Completed Topics: {completed_count}/{total}")

        percentage = int(progress * 100)

        st.write(f"Progress Percentage: {percentage}%")

        if percentage == 100:
            st.success("🎉 All Topics Completed!")
