import random
import streamlit as st
from logic_utils import check_guess, get_range_for_difficulty, parse_guess, update_score

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")


def start_new_game():
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    st.session_state.status = "playing"
    st.session_state.score = 0
    st.session_state.history = []


# FIX (AI collab): the first game started with attempts = 1 while New Game used 0 (so "Attempts
# Left" was off by one), and switching difficulty kept a secret from the old range. Claude Code
# routed first load, New Game, and difficulty changes through one start_new_game() with attempts = 0.
if "secret" not in st.session_state or st.session_state.get("difficulty") != difficulty:
    start_new_game()
    st.session_state.difficulty = difficulty

st.subheader("Make a guess")

# FIX (AI collab): the "1 and 100" text was hardcoded, and the info/debug panels were drawn before
# a guess was processed, so Attempts Left and Score were one guess behind. Claude Code moved them
# into placeholders that are redrawn after the guess is handled, using the real range.
status_box = st.empty()
debug_box = st.empty()


def render_status():
    status_box.info(
        f"Guess a number between {low} and {high}. "
        f"Attempts left: {attempt_limit - st.session_state.attempts}"
    )
    with debug_box.container():
        with st.expander("Developer Debug Info"):
            st.write("Secret:", st.session_state.secret)
            st.write("Attempts:", st.session_state.attempts)
            st.write("Score:", st.session_state.score)
            st.write("Difficulty:", difficulty)
            st.write("History:", st.session_state.history)


raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

# FIX (AI collab): New Game left status as "won"/"lost" (so st.stop() below blocked play), kept
# the old score/history, and ignored difficulty. Claude Code traced the stuck state to the
# unreset status; it now resets all of them and draws the secret from the difficulty's range.
if new_game:
    start_new_game()
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    render_status()
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    ok, guess_int, err = parse_guess(raw_guess, low, high)

    # FIX (AI collab): invalid input (blank, text, decimal, out of range) used up an attempt.
    # Claude Code now counts an attempt only for a valid guess.
    if not ok:
        st.error(err)
    else:
        st.session_state.attempts += 1
        st.session_state.history.append(guess_int)

        # FIX (AI collab): the secret was converted to a str on even attempts, so guesses were
        # compared as text. Claude Code spotted it while listing bugs; the secret is now always an int.
        secret = st.session_state.secret

        outcome, message = check_guess(guess_int, secret)

        if show_hint:
            st.warning(message)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

render_status()

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
