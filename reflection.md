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
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
