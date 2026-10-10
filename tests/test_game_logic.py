import pytest

from logic_utils import check_guess


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
