# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
  1. On my first play, I immediately got into a situation where the hints were nonsensical, and spent the remaining guesses quickly to get into another game to check more bugs. Unfortunately, the New Game button also was nonfunctional, forcing me to refresh the page. Something I noticed on refresh is that the amount of Attempts Left also changed, 7 on new load, 8 on pressing New Game.
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").
  1. Got the "Out of Attempts" message while still having "Attempts Left: 1" in the prompt. Would expect Attempts Left to be 0 when out of attempts.
  2. Got "Go LOWER!" on guessing 41, and "Go HIGHER!" on guessing 40, while the actual number was 9. Would expect both to say "Go LOWER!".
  3. Score in the bottom prompt is -35, while in developer debug info, it is -30. Would expect these to match.
  4. There is no sanitation on input. Guesses can be out of range or decimal values in range. Would expect both of these to not be allowed.
  5. The New Game button does not work as expected after losing a game (the secret number restarts but no attempts are given, despit the prompt saying otherwise). Even upon winning a game, you are unable to play. Would expect a full game reset, allowing you to play another game, regardless of the state of the previous game.

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input         | Expected Behavior               | Actual Behavior                 | Console Output / Error |
|---------------|---------------------------------|---------------------------------|------------------------|
| 40,41         | Go Lower for both  (ans<40)     | Higher, Lower                   | none                   |
| New Game      | Start with 7 Attempts in prompt | Start with 8 Attempts in prompt | none                   |
| NG after loss | The game resets fully           | cannot enter more numbers       | none                   |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
  - I used Claude Code (in VS Code) as an agent that read the project, edited files, and ran pytest.
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
  - **Suggestion:** The AI read `check_guess` and pointed out that the hints were inverted: a guess above the secret returned "Go HIGHER!" and a guess below it returned "Go LOWER!". It swapped the messages so a too-high guess says "Go LOWER!" and a too-low guess says "Go HIGHER!".
  - **Correct:** Yes. This matched the bug I saw while playing (guessing 41 and 40 against a secret of 9 gave opposite hints).
  - **Verified:** I had the AI write a parametrized pytest, `test_check_guess`, which checks the outcome and that the message contains the right direction and not the opposite one. It passes (3 passed with `python -m pytest`).
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.
  - **Suggestion:** When I got `ModuleNotFoundError: No module named 'logic_utils'` running the test file directly, the AI added a `pytest.ini` (`pythonpath = .`) so imports would resolve from any folder.
  - **Incorrect/unnecessary:** It worked, but it was out of scope. The error came from how I ran the tests (running the file instead of `pytest`), not from a problem in the project, so the extra config file wasn't needed.
  - **Verified:** I asked the AI to remove the file, and `python -m pytest` from the project root still passes (3 passed).

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
  - I compared against the expected behavior I wrote in the bug log (for example, "Go LOWER for both guesses") and re-ran the same case after each fix. For logic bugs, I also wanted an automated test so the bug can't quietly come back.
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
  - I ran `python -m pytest` on `tests/test_game_logic.py`. The starter tests failed at first because they compared the whole result to a string like `"Too High"`, but `check_guess` returns a tuple `(outcome, message)`. That showed the tests were wrong, not the function, so I consolidated them into one parametrized test that unpacks the tuple and also checks the hint direction. I then added tests for the difficulty ranges, input parsing (decimals, out-of-range, empty, text), and scoring, and all 36 tests pass.
  - I played the game normally, while using the developer debug info to test correct functionality. When receiving a secret of 93, I guessed 92 to confirm "Go HIGHER!", twice in a row to confirm the strange behavior on even guesses, then I guessed 94 to confirm "Go LOWER!" appears, again twice. Afterwards, I guessed 92, winning the game, and hit New Game to confirm playing again was now possible.
- Did AI help you design or understand any tests? How?
  - Yes. The AI explained why the starter tests failed (tuple vs. string), wrote the consolidated parametrized test, and explained that the `ModuleNotFoundError` came from how I ran the file; running `python -m pytest` from the project root fixes it.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
  - Every time you click a button or type in a box, Streamlit re-runs the whole Python script from top to bottom, so normal variables are thrown away and recreated each time. `st.session_state` is a dictionary that survives those reruns, so it is where the game keeps the secret number, attempts, score, and status. Code that runs top to bottom also draws things in order, which caused a bug in this project: the "Attempts left" and score panels were drawn before the guess was processed, so they showed old values until I redrew them after handling the guess.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
  - Writing down expected vs. actual behavior for each bug first, then adding a test that fails on the bug and passes on the fix. It made it easy to tell when a bug was really gone, and the tests keep it from quietly coming back.
- What is one thing you would do differently next time you work with AI on a coding task?
  - I would give the AI a tighter scope for each request and review each change before moving on. The unneeded `pytest.ini` was a small example, and at one point the AI's fix for a Hard difficulty bug (a bigger range with the same 5 attempts) made that level almost unwinnable. I only caught that because I asked whether any bugs remained.
- In one or two sentences, describe how this project changed the way you think about AI generated code.
  - AI generated code can look clean and still be wrong in small ways, like inverted hints or a secret that turns into a string on every other guess, so it needs to be played and tested, not just read. The same goes for AI fixes, which need their own tests.
