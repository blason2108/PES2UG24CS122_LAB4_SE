# High-Low Card Predictor Repair Lab

This project is a card prediction game using **Pygame**. It introduces students to deck state management, lexicographical vs. numerical evaluation, probability assessment, and UI button interaction within an object-oriented codebase.
---

## What's Provided

A working High or Low Card Predictor game with:

- A complete 52-card deck model supporting suits, ranks, and auto-reshuffling when depleted
- Procedural card rendering featuring suit symbols and colors (Hearts, Diamonds, Clubs, Spades)
- Clickable HIGHER and LOWER interactive buttons
- Live score tracking, deck count indicators, and round feedback messaging

It has **one deliberate bug** and **three optional features** left as tasks to implement. You are expected to **analyze**, **interact with an AI assistant**, and **complete/fix** the game to make it fully functional and more interesting.

### **Use an LLM (e.g. ChatGPT or Claude) as your debugging and pair-programming partner for this lab.**
---

## Getting Started

### Setup

1. Make sure you have Python 3.10+ installed.
2. Install dependencies:

```bash
pip install pygame
```

3. Run the game:

```bash
python main.py
```

**Controls:** Left-click on the HIGHER or LOWER buttons to predict the next card.   


## Tasks to Complete

Each task must be completed using an iterative process involving LLM suggestions and your critical code review.

### Task 1: Fix the card rank comparison bug

When predicting whether the next card is higher or lower, face cards and tens behave inconsistently. In game_engine.evaluate_guess(), the comparison uses rank_str (e.g., comparing string "10" against "9", or "K" against "Q") instead of comparing numeric ranks. Because strings are compared lexicographically in Python, "10" is evaluated as smaller than "2". Fix the evaluation logic to use numeric_rank so ranks are strictly compared as numbers.

### Task 2: Implement a win streak multiplier

Currently, each correct guess only gives a flat +1 point. Implement a streak tracker in game_engine that monitors consecutive correct predictions. Award bonus multipliers or escalating points for maintaining a streak (e.g., 2x points at 3 wins in a row, 3x at 5 wins), and reset the streak counter back to zero on an incorrect guess.

### Task 3: Implement tie / push handling

When the drawn card has the exact same rank as the current card (e.g., 7 of Hearts followed by 7 of Spades), the guess is automatically penalized as incorrect. Implement custom tie/push rules: preserve the player's score and streak, and display a yellow "PUSH / TIE! Rank matched." message rather than deducting a point.

### Task 4: Implement side-by-side card reveal animation

Currently, the current card immediately switches to the new card on guess submission. Modify game_engine.render() to display both cards side-by-side (the previous card on the left and the newly revealed card on the right) with a brief pause or transition before shifting to the next round, giving the player time to visually confirm both cards.

---

## Expected Behavior

- Clicking HIGHER or LOWER draws the next card from the deck and updates the score.
- Number and face cards evaluate according to their real hierarchy (2 < 3 <...< K < A).
- The deck counter accurately decrements with each draw and reshuffles automatically when empty. 
- Visual feedback clearly displays whether the previous guess was correct or incorrect.
---

## Folder Structure

```
card_predictor/
├── game/
│   ├── card.py
│   ├── deck.py
│   └── game_engine.py
├── main.py
└── README.md
```

---

## Submission Checklist

Submission is only the following three things:

- [] A 10-second video of gameplay **before** your changes, showing the bug/broken behavior
- [] A 10-second video of gameplay **after** your changes, showing the bug fixed and the new features working
- [] The Chat/LLM used page link, with the complete chat history
# PES2UG24CS122_LAB4_SE
