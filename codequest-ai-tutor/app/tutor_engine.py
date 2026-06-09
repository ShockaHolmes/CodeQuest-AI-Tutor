from __future__ import annotations

from dataclasses import dataclass


@dataclass
class TutorResponse:
    message: str
    is_correct: bool | None = None
    badge_awarded: str | None = None


class AITutorEngine:
    """
    A simple AI-style tutor engine.

    This does not require an external AI API. It uses structured lesson data and
    friendly rules to guide students step by step. Later, this class can be
    expanded to call a real AI service.
    """

    def welcome_student(self, name: str, track: str) -> str:
        return (
            f"Welcome, {name}! I am CodeQuest, your coding guide. "
            f"You are starting the {track} path. We will learn one small step at a time."
        )

    def explain_lesson(self, lesson: dict) -> str:
        steps = lesson.get("steps", [])
        step_text = "\n".join([f"{index + 1}. {step}" for index, step in enumerate(steps)])
        return (
            f"Today we are learning: {lesson['title']}\n\n"
            f"Goal: {lesson['goal']}\n\n"
            f"Let us break it down:\n{step_text}"
        )

    def give_hint(self, lesson: dict) -> str:
        return f"Hint: {lesson.get('hint', 'Try reading the example one more time.')}"

    def check_quiz_answer(self, lesson: dict, student_answer: str) -> TutorResponse:
        correct_answer = lesson["quiz"]["answer"].strip().lower()
        normalized_answer = student_answer.strip().lower()

        if normalized_answer == correct_answer:
            return TutorResponse(
                message="Great job! You got it right. You are building strong coding skills.",
                is_correct=True,
                badge_awarded=lesson.get("badge"),
            )

        return TutorResponse(
            message=(
                "Not quite, but that is how learning works. "
                f"The correct answer is: {lesson['quiz']['answer']}. "
                "Try the practice challenge again and look for the pattern."
            ),
            is_correct=False,
        )

    def age_to_track(self, age: int) -> str:
        if age <= 10:
            return "Explorer"
        if age <= 13:
            return "Builder"
        return "Creator"
