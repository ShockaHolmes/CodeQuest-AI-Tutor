# CodeQuest AI Tutor

**CodeQuest AI Tutor** is a beginner-friendly Python learning app for kids ages 8–17. It teaches coding step by step with an AI-style assistant, interactive lessons, quizzes, practice challenges, badges, and progress tracking.

The project is designed for classrooms, after-school STEM programs, coding clubs, and self-paced learning.

---

## What the App Does

CodeQuest AI Tutor helps students learn coding by:

- Explaining lessons in simple language
- Breaking coding ideas into small steps
- Giving age-friendly examples
- Asking quiz questions
- Giving hints when students get stuck
- Checking answers
- Awarding badges
- Saving student progress locally

The app can run without an internet AI service using the built-in tutor engine. You can later connect it to a real AI model if desired.

---

## Student Age Groups

The app supports three learning tracks:

| Track | Ages | Focus |
|---|---:|---|
| Explorer | 8–10 | Computer basics, patterns, simple Python |
| Builder | 11–13 | Variables, input, conditionals, loops |
| Creator | 14–17 | Functions, lists, mini projects, problem solving |

---

## Tech Stack

- Python 3.10+
- Streamlit for the web app interface
- JSON for lessons and student progress
- Pytest for testing

---

## Project Structure

```text
kids_code_ai_tutor/
├── app/
│   ├── main.py              # Streamlit app
│   ├── tutor_engine.py      # AI-style assistant logic
│   ├── progress.py          # Save/load progress
│   └── lesson_loader.py     # Loads lessons from JSON
├── lessons/
│   └── python_basics.json   # Lesson content
├── data/
│   └── students.json        # Created automatically when app runs
├── tests/
│   └── test_tutor_engine.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## How to Run the App

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/kids-code-ai-tutor.git
cd kids-code-ai-tutor
```

### 2. Create a virtual environment

Mac/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install requirements

```bash
pip install -r requirements.txt
```

If you are not activating the virtual environment in your shell, use the local environment directly:

```bash
./.venv/bin/pip install -r requirements.txt
```

### 4. Run the app

```bash
streamlit run app/main.py
```

Or run Streamlit through the project-local Python interpreter:

```bash
./.venv/bin/python -m streamlit run app/main.py
```

On macOS, you can also double-click [start.command](/Users/shocka/CodeQuest-AI-Tutor/start.command) from the workspace root to start the app and open the dashboard automatically.

---

## Lesson Design

Each lesson has:

- A title
- Age track
- Learning goal
- Step-by-step explanation
- Example code
- Practice task
- Quiz question
- Hint
- Badge reward

Lessons are stored in JSON so teachers can add more lessons without changing the app code.

---

## Example Lesson Flow

1. Student chooses their name and age group.
2. The AI Tutor introduces the lesson.
3. Student reads the step-by-step explanation.
4. Student studies the example code.
5. Student completes a practice challenge.
6. Student answers a quiz question.
7. The tutor gives feedback and awards a badge.

---

## Future Features

- Login system for multiple classrooms
- Teacher dashboard
- Student certificates
- More lessons for Python, HTML, CSS, JavaScript, and game development
- AI-generated hints using OpenAI or another AI service
- Voice narration for younger students
- Accessibility mode
- Offline classroom version

---

## License

MIT License
