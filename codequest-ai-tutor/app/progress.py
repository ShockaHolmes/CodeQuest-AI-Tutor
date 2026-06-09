import json
from pathlib import Path
from typing import Any

DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "students.json"


def load_progress() -> dict[str, Any]:
    if not DATA_FILE.exists():
        return {}
    with DATA_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_progress(progress: dict[str, Any]) -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(progress, file, indent=2)


def update_student_progress(name: str, lesson_id: str, badge: str | None) -> dict[str, Any]:
    progress = load_progress()
    student = progress.setdefault(name, {"completed_lessons": [], "badges": []})

    if lesson_id not in student["completed_lessons"]:
        student["completed_lessons"].append(lesson_id)

    if badge and badge not in student["badges"]:
        student["badges"].append(badge)

    save_progress(progress)
    return student
