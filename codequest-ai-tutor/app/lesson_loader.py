import json
from pathlib import Path
from typing import Any

LESSON_FILE = Path(__file__).resolve().parents[1] / "lessons" / "python_basics.json"


def load_lessons() -> list[dict[str, Any]]:
    """Load lesson data from the lessons folder."""
    with LESSON_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def get_lessons_by_track(track: str) -> list[dict[str, Any]]:
    """Return only the lessons that match the selected student track."""
    lessons = load_lessons()
    return [lesson for lesson in lessons if lesson["track"] == track]
