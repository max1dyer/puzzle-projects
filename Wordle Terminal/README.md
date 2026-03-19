# Terminal Wordle (Python)

A terminal-based version of Wordle built in Python.  
This project recreates Wordle's guessing mechanics and color-coded feedback.

---

## Features

- Play Wordle directly in the terminal
- Input validation for valid 5-letter words
- Color-coded feedback using `colorama`:
  - 🟩 Green: correct letter in correct position
  - 🟨 Yellow: correct letter in wrong position
  - ⬜ Gray: letter not in the word
- Handles duplicate letters correctly by tracking number of letters in each word
- 6 attempts per game (like the original Wordle)
- Random word selection from a customizable word list

---

## How It Works

- Words are loaded from a text file (`wordle_words.txt`)
- The game selects a random word as the answer
- Each guess is validated against the word list
- An algorithm passes over the guessed word twice to assign colors:
  1. First pass: identifies correct letters in correct positions (green)
  2. Second pass: identifies correct letters in wrong positions (yellow), accounting for duplicate letters

---

## Technologies Used

- Python 3
- `colorama` for terminal coloring

---

## How to Run

1. Install colorama if not already installed:
```bash
pip install colorama

2. Clone this repository:

```bash
git clone https://github.com/yourusername/wordle-terminal
cd wordle-terminal

3. Compile and run

---

## Example

<img width="329" height="143" alt="wordle_terminal_ss" src="https://github.com/user-attachments/assets/86ea7c31-32e1-4ddb-ad4d-ee3d9fde39e9" />

