from app.tutor_engine import AITutorEngine


def test_age_to_track():
    engine = AITutorEngine()
    assert engine.age_to_track(8) == "Explorer"
    assert engine.age_to_track(12) == "Builder"
    assert engine.age_to_track(16) == "Creator"


def test_correct_answer_awards_badge():
    engine = AITutorEngine()
    lesson = {
        "quiz": {"answer": "print"},
        "badge": "First Line Coder",
    }
    response = engine.check_quiz_answer(lesson, "PRINT")
    assert response.is_correct is True
    assert response.badge_awarded == "First Line Coder"


def test_wrong_answer_no_badge():
    engine = AITutorEngine()
    lesson = {
        "quiz": {"answer": "print"},
        "badge": "First Line Coder",
    }
    response = engine.check_quiz_answer(lesson, "variable")
    assert response.is_correct is False
    assert response.badge_awarded is None
