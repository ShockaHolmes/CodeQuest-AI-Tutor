import streamlit as st

from lesson_loader import get_lessons_by_track
from progress import load_progress, update_student_progress
from tutor_engine import AITutorEngine
from voice import has_elevenlabs_key, synthesize_speech

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

    st.divider()
    st.header("Voice Assistant")
    voice_enabled = st.toggle("Read questions aloud", value=False)
    auto_read_quiz = st.toggle(
        "Auto-read quiz on lesson change",
        value=False,
        disabled=not voice_enabled,
    )
    voice_id = st.text_input(
        "ElevenLabs Voice ID",
        value="kdmDKE6EkgrWrrykO9Qt",
        help="Set the voice ID from your ElevenLabs account.",
    )
    api_key_available = has_elevenlabs_key()
    if api_key_available:
        st.caption("ElevenLabs key detected.")
    else:
        st.warning("Set ELEVENLABS_API_KEY in your environment to enable voice.")

    if st.button(
        "Test ElevenLabs Connection",
        key="test_elevenlabs",
        disabled=not api_key_available,
        help="Runs a quick text-to-speech request to verify your API key.",
    ):
        test_speech = synthesize_speech(
            "Connection test from CodeQuest.",
            voice_id=voice_id,
        )
        if test_speech.audio_bytes:
            st.success("ElevenLabs connection successful.")
        else:
            st.error(test_speech.error_message)

voice_ready = voice_enabled and api_key_available

st.info(engine.welcome_student(name, track))

lessons = get_lessons_by_track(track)
lesson_titles = [lesson["title"] for lesson in lessons]
selected_title = st.selectbox("Choose a lesson", lesson_titles)
lesson = next(item for item in lessons if item["title"] == selected_title)

if voice_ready and auto_read_quiz:
    previous_lesson_id = st.session_state.get("last_auto_read_lesson_id")
    current_lesson_id = lesson["id"]
    if previous_lesson_id != current_lesson_id:
        speech = synthesize_speech(lesson["quiz"]["question"], voice_id=voice_id)
        if speech.audio_bytes:
            st.session_state["last_auto_read_lesson_id"] = current_lesson_id
            st.session_state["auto_quiz_audio"] = speech.audio_bytes
            st.session_state["auto_quiz_error"] = None
        else:
            st.session_state["auto_quiz_audio"] = None
            st.session_state["auto_quiz_error"] = speech.error_message
elif not auto_read_quiz:
    st.session_state["auto_quiz_audio"] = None
    st.session_state["auto_quiz_error"] = None
    st.session_state["last_auto_read_lesson_id"] = None

left, right = st.columns([2, 1])

with left:
    st.header(lesson["title"])
    st.write(f"**Goal:** {lesson['goal']}")

    st.markdown("### Step-by-Step Lesson")
    instructions_text = " ".join(
        [
            f"Step {index}. {step}"
            for index, step in enumerate(lesson["steps"], start=1)
        ]
    )
    if st.button(
        "Read Lesson Instructions",
        key="read_instructions",
        disabled=not voice_ready,
        help="Enable voice in the sidebar and set ELEVENLABS_API_KEY.",
    ):
        speech = synthesize_speech(instructions_text, voice_id=voice_id)
        if speech.audio_bytes:
            st.audio(speech.audio_bytes, format="audio/mpeg")
        else:
            st.error(speech.error_message)

    for index, step in enumerate(lesson["steps"], start=1):
        st.write(f"**Step {index}:** {step}")

    st.markdown("### Example Code")
    st.code(lesson["example_code"], language="python")

    st.markdown("### Practice Challenge")
    st.write(lesson["practice"])
    if voice_enabled:
        if st.button("Read Practice Challenge", key="read_practice"):
            speech = synthesize_speech(lesson["practice"], voice_id=voice_id)
            if speech.audio_bytes:
                st.audio(speech.audio_bytes, format="audio/mpeg")
            else:
                st.error(speech.error_message)

    student_code = st.text_area("Write your practice code here", height=140)

    if st.button("Ask CodeQuest for a Hint"):
        st.warning(engine.give_hint(lesson))

with right:
    st.markdown("### Quiz")
    st.write(lesson["quiz"]["question"])
    if voice_enabled and auto_read_quiz:
        if st.session_state.get("auto_quiz_audio"):
            st.audio(st.session_state["auto_quiz_audio"], format="audio/mpeg")
        elif st.session_state.get("auto_quiz_error"):
            st.error(st.session_state["auto_quiz_error"])
    if voice_enabled:
        if st.button("Read Quiz Question", key="read_quiz"):
            speech = synthesize_speech(lesson["quiz"]["question"], voice_id=voice_id)
            if speech.audio_bytes:
                st.audio(speech.audio_bytes, format="audio/mpeg")
            else:
                st.error(speech.error_message)

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
