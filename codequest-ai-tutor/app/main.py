import streamlit as st

from lesson_loader import get_lessons_by_track
from progress import load_progress, update_student_progress
from tutor_engine import AITutorEngine

st.set_page_config(page_title="CodeQuest AI Tutor", page_icon="🧠", layout="wide")

engine = AITutorEngine()

st.title("🧠 CodeQuest AI Tutor")
st.subheader("A step-by-step coding teacher for kids ages 8–17")

with st.sidebar:
    st.header("Student Setup")
    name = st.text_input("Student name", value="Student")
    age = st.number_input("Student age", min_value=8, max_value=17, value=10)
    track = engine.age_to_track(age)
    st.success(f"Learning Track: {track}")

    progress = load_progress().get(name, {"completed_lessons": [], "badges": []})
    st.metric("Completed Lessons", len(progress["completed_lessons"]))
    st.write("Badges:")
    if progress["badges"]:
        for badge in progress["badges"]:
            st.write(f"🏅 {badge}")
    else:
        st.write("No badges yet. Complete a lesson to earn one!")

st.info(engine.welcome_student(name, track))

lessons = get_lessons_by_track(track)
lesson_titles = [lesson["title"] for lesson in lessons]
selected_title = st.selectbox("Choose a lesson", lesson_titles)
lesson = next(item for item in lessons if item["title"] == selected_title)

left, right = st.columns([2, 1])

with left:
    st.header(lesson["title"])
    st.write(f"**Goal:** {lesson['goal']}")

    st.markdown("### Step-by-Step Lesson")
    for index, step in enumerate(lesson["steps"], start=1):
        st.write(f"**Step {index}:** {step}")

    st.markdown("### Example Code")
    st.code(lesson["example_code"], language="python")

    st.markdown("### Practice Challenge")
    st.write(lesson["practice"])
    student_code = st.text_area("Write your practice code here", height=140)

    if st.button("Ask CodeQuest for a Hint"):
        st.warning(engine.give_hint(lesson))

with right:
    st.markdown("### Quiz")
    st.write(lesson["quiz"]["question"])
    answer = st.text_input("Your answer")

    if st.button("Check My Answer"):
        response = engine.check_quiz_answer(lesson, answer)
        if response.is_correct:
            st.success(response.message)
            student_progress = update_student_progress(name, lesson["id"], response.badge_awarded)
            st.balloons()
            if response.badge_awarded:
                st.write(f"🏅 Badge earned: **{response.badge_awarded}**")
        else:
            st.error(response.message)

    st.markdown("### Tutor Explanation")
    if st.button("Explain This Lesson Again"):
        st.text(engine.explain_lesson(lesson))

st.divider()
st.caption("Teacher note: Add more lessons by editing lessons/python_basics.json.")
