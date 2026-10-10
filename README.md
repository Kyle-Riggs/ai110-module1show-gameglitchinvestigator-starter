# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- **Game purpose:** a number-guessing game built with Streamlit. The game picks a secret number in a range set by the difficulty (Easy 1–20, Normal 1–100, Hard 1–200). You guess within a limited number of attempts, get a "Go HIGHER!" or "Go LOWER!" hint after each guess, and earn or lose points.
- **Bugs found:**
  - The hints were inverted.
  - On every other guess the secret was converted to a string, so guesses were compared as text.
  - New Game didn't reset the game state, so after a win or loss you couldn't play again, and the secret ignored the difficulty.
  - The first game started with one attempt already used, so "Attempts left" was off by one.
  - The range text always said "1 and 100", and the "Attempts left" and score panels lagged one guess behind.
  - Guesses weren't validated: decimals were truncated and out-of-range numbers were accepted.
  - Scoring was inconsistent: wins cost an extra attempt, and a too-high guess gave +5 on even attempts but -5 on odd ones.
  - Hard difficulty had a smaller range than Normal.
- **Fixes applied:**
  - Swapped the hints and always compare numbers.
  - New Game, first load, and changing difficulty all go through one `start_new_game()` that resets everything.
  - The status panels are redrawn after each guess.
  - Guesses must be whole numbers inside the range, and invalid input no longer uses an attempt.
  - Scoring is now `100 - 10 × attempt` for a win (minimum 10) and -5 for any wrong guess.
  - Hard is now the largest range.
  - The game logic moved from `app.py` into `logic_utils.py`, with pytest tests for it in `tests/`.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. Run `python -m streamlit run app.py`. The sidebar shows the difficulty (default Normal), the range (1 to 100), and the attempts allowed (8). The banner reads "Guess a number between 1 and 100. Attempts left: 8".
2. Open "Developer Debug Info" to see the secret number. Say the secret is 93.
3. Enter `5.5` or `150` and press Submit. The game shows an error ("Enter a whole number (no decimals)." or "Guess must be between 1 and 100.") and Attempts left stays at 8.
4. Enter `92`. The game says "📈 Go HIGHER!", Attempts left drops to 7, and the score is -5. Enter `94`: "📉 Go LOWER!". The hints are the same on odd and even guesses.
5. Enter `93`. Balloons appear and the game shows "You won! The secret was 93." with the final score (a win on attempt 3 after two wrong guesses is 70 - 10 = 60).
6. Press New Game. Attempts, score and history reset, and a new secret is drawn from the current difficulty's range, so you can play again right away. Changing the difficulty in the sidebar also starts a fresh game.
7. Use up all your attempts with wrong guesses. The game shows "Out of attempts!" with the secret and the score, "Attempts left" shows 0, and New Game starts a fresh game.

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
$ python -m pytest
============================= test session starts =============================
platform win32 -- Python 3.13.15, pytest-9.1.1, pluggy-1.6.0
rootdir: ...\ai110-module1show-gameglitchinvestigator-starter
plugins: anyio-4.15.1
collected 36 items

tests\test_game_logic.py ....................................            [100%]

============================= 36 passed in 0.69s ==============================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
