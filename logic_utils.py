def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    # FIX (AI collab): Hard (1-50) was a smaller range than Normal (1-100), so it was easier.
    # Claude Code flagged it while reviewing the code; Hard is now the largest range (1-200).
    if difficulty == "Hard":
        return 1, 200
    return 1, 100


def parse_guess(raw: str, low: int = None, high: int = None):
    """
    Parse user input into an int guess, optionally checking it is within [low, high].

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    raw = raw.strip()
    if raw == "":
        return False, None, "Enter a guess."

    # FIX (AI collab): decimals were silently truncated (5.9 became 5) and out-of-range guesses
    # were accepted. Claude Code rewrote this to reject decimals and values outside [low, high].
    try:
        value = int(raw)
    except ValueError:
        try:
            float(raw)
        except ValueError:
            return False, None, "That is not a number."
        return False, None, "Enter a whole number (no decimals)."

    if low is not None and high is not None and not (low <= value <= high):
        return False, None, f"Guess must be between {low} and {high}."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    # FIX (AI collab): hints were inverted (too-high said "Go HIGHER!"). Claude Code swapped them,
    # moved check_guess here from app.py, and removed the string-comparison fallback that only
    # existed for the even-attempt str bug. tests/test_game_logic.py checks the hint text.
    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    # FIX (AI collab): a win cost an extra attempt (attempt_number + 1), and "Too High" awarded +5
    # on even attempts but -5 on odd ones. Claude Code made wins score 100 - 10 * attempt_number
    # (min 10) and made "Too High" always -5, matching "Too Low".
    if outcome == "Win":
        points = 100 - 10 * attempt_number
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score
