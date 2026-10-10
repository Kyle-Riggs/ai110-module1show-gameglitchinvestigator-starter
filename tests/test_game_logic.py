import pytest

from logic_utils import check_guess, get_range_for_difficulty, parse_guess, update_score


# check_guess returns (outcome, message). Hints were inverted before the fix, so each case
# also checks the message: a too-high guess says go LOWER, a too-low guess says go HIGHER.
@pytest.mark.parametrize(
    "guess, secret, expected_outcome, expected_hint",
    [
        (50, 50, "Win", "Correct"),
        (60, 50, "Too High", "LOWER"),
        (40, 50, "Too Low", "HIGHER"),
    ],
)
def test_check_guess(guess, secret, expected_outcome, expected_hint):
    outcome, message = check_guess(guess, secret)
    assert outcome == expected_outcome
    assert expected_hint in message
    # The opposite direction must never appear in the hint
    for wrong in {"LOWER", "HIGHER"} - {expected_hint}:
        assert wrong not in message


# Difficulty ranges: Hard used to be 1-50, smaller (easier) than Normal's 1-100.
@pytest.mark.parametrize(
    "difficulty, expected",
    [("Easy", (1, 20)), ("Normal", (1, 100)), ("Hard", (1, 200)), ("Unknown", (1, 100))],
)
def test_get_range_for_difficulty(difficulty, expected):
    assert get_range_for_difficulty(difficulty) == expected


def test_hard_range_is_larger_than_normal_and_easy():
    def size(difficulty):
        low, high = get_range_for_difficulty(difficulty)
        return high - low

    assert size("Easy") < size("Normal") < size("Hard")


# Input parsing: decimals used to be truncated (5.9 -> 5) and out-of-range guesses were accepted.
@pytest.mark.parametrize("raw, expected", [("7", 7), (" 42 ", 42), ("1", 1), ("100", 100)])
def test_parse_guess_accepts_valid_whole_numbers(raw, expected):
    assert parse_guess(raw, 1, 100) == (True, expected, None)


@pytest.mark.parametrize("raw", ["5.9", "5.0", "1e1"])
def test_parse_guess_rejects_decimals(raw):
    ok, value, error = parse_guess(raw, 1, 100)
    assert not ok and value is None
    assert "whole number" in error


@pytest.mark.parametrize("raw", ["0", "101", "-5"])
def test_parse_guess_rejects_out_of_range(raw):
    ok, value, error = parse_guess(raw, 1, 100)
    assert not ok and value is None
    assert "between 1 and 100" in error


@pytest.mark.parametrize("raw", [None, "", "   "])
def test_parse_guess_rejects_empty(raw):
    assert parse_guess(raw, 1, 100) == (False, None, "Enter a guess.")


def test_parse_guess_rejects_text():
    assert parse_guess("abc", 1, 100) == (False, None, "That is not a number.")


# Scoring: wins used to cost an extra attempt (attempt_number + 1) and "Too High" gave +5 on
# even attempts but -5 on odd ones.
@pytest.mark.parametrize(
    "attempt, expected_points",
    [(1, 90), (2, 80), (5, 50), (9, 10), (20, 10)],
)
def test_update_score_win_points(attempt, expected_points):
    assert update_score(0, "Win", attempt) == expected_points


@pytest.mark.parametrize("attempt", [1, 2, 3, 4])
@pytest.mark.parametrize("outcome", ["Too High", "Too Low"])
def test_update_score_wrong_guess_always_costs_five(outcome, attempt):
    assert update_score(50, outcome, attempt) == 45


def test_update_score_unknown_outcome_keeps_score():
    assert update_score(30, "Other", 1) == 30
