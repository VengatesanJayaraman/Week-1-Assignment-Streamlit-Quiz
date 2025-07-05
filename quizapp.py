import streamlit as st
import csv
import os
import time

# --- Helper functions ---
def load_quiz_data():
    return [
        {
            "question": "What is the capital of India?",
            "options": ["Mumbai", "Delhi", "Chennai", "Kolkata"],
            "answer": "Delhi"
        },
        {
            "question": "Who is known as the Father of the Indian Constitution?",
            "options": ["Gandhi", "Ambedkar", "Nehru", "Tagore"],
            "answer": "Ambedkar"
        },
        {
            "question": "Which Indian state has the longest coastline?",
            "options": ["Kerala", "Gujarat", "Andhra Pradesh", "Tamil Nadu"],
            "answer": "Gujarat"
        }
    ]

def save_answer(username, question, selected, correct):
    file_path = "answers.csv"
    file_exists = os.path.isfile(file_path)

    with open(file_path, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Username", "Question", "Selected Answer", "Correct Answer"])
        writer.writerow([username, question, selected, correct])

# --- Streamlit UI ---
st.set_page_config(page_title="🇮🇳 India Quiz", layout="centered")
st.title("🇮🇳 India Quiz App")

# --- Login ---
if "username" not in st.session_state:
    username = st.text_input("Enter your name to begin the quiz:")
    if username:
        st.session_state.username = username
        st.session_state.question_index = 0
        st.session_state.score = 0
        st.session_state.start_time = time.time()
        st.session_state.current_q = -1
        st.rerun()
    st.stop()

quiz_data = load_quiz_data()
index = st.session_state.question_index
TIMER_LIMIT = 30  # seconds

if index < len(quiz_data):
    q = quiz_data[index]

    # Reset timer if new question
    if st.session_state.current_q != index:
        st.session_state.start_time = time.time()
        st.session_state.answered = False
        st.session_state.current_q = index

    elapsed = int(time.time() - st.session_state.start_time)
    time_left = max(0, TIMER_LIMIT - elapsed)
    progress = time_left / TIMER_LIMIT

    st.subheader(f"Q{index + 1}: {q['question']}")
    user_answer = st.radio("Choose your answer:", q["options"], key=f"q{index}")
    st.markdown(f"⏳ **Time left: {time_left} seconds**")
    st.progress(progress)

    # Auto-submit
    if time_left == 0 and not st.session_state.answered:
        selected = "No Answer"
        correct = q["answer"]
        save_answer(st.session_state.username, q["question"], selected, correct)
        st.session_state.question_index += 1
        st.rerun()

    # Manual submit
    if st.button("Submit Answer") and not st.session_state.answered:
        selected = user_answer
        correct = q["answer"]
        if selected == correct:
            st.success("✅ Correct!")
            st.session_state.score += 1
        else:
            st.error(f"❌ Wrong! Correct answer: {correct}")

        save_answer(st.session_state.username, q["question"], selected, correct)
        st.session_state.answered = True
        time.sleep(2)
        st.session_state.question_index += 1
        st.rerun()
else:
    st.success("🎉 You've completed the quiz!")
    st.markdown(f"👤 **User:** {st.session_state.username}")
    st.markdown(f"🏆 **Score:** {st.session_state.score} / {len(quiz_data)}")
    st.markdown("---")
    if st.button("Restart Quiz"):
        del st.session_state.username
        st.rerun()
