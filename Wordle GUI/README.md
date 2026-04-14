# Wordle GUI

A desktop version of the popular Wordle game built in **Python** using **Tkinter**.  
This project recreates the Wordle gameplay experience with an interactive GUI, animated feedback, and both physical/on-screen keyboard support.

---

## Features

- 6x5 Wordle game board
- Physical keyboard input support
- On-screen clickable keyboard
- Tile color feedback:
  - 🟩 Green = Correct letter, correct position
  - 🟨 Yellow = Correct letter, wrong position
  - ⬜ Gray = Letter not in word
- Animated tile reveal
- Invalid guess shake animation
- Popup feedback messages
- Restart button for new games
- Duplicate-letter handling matching Wordle rules

---

## How it Works

### Game Logic

- Randomly selects word from valid words list (`wordle_words.txt`)
- Each guess is validated against the word list
- An algorithm passes over the guessed word twice to assign colors:
  1. First pass: identifies correct letters in correct positions (green)
  2. Second pass: identifies correct letters in wrong positions (yellow), accounting for duplicate letters
 
### GUI Features

- Tiles update dynamically with each letter entered
- Invalid guesses trigger shaking animation
- Pressing `Enter` triggers a popup to display status
- On-screen keyboard is updated with color feedback

---

## Future Expansions

- Resizable/scrollable window for smaller screen sizes
- Add win statistics
- Different themes (ex: dark mode)
- Sound effects
- Daily challenges

---

## What I Learned

This project helped me strengthen my skills in:
- Event-driven GUI programming
- Animation and user feedback
- State management in interactive applications
- Handling timed GUI changes
- Object-oriented Python design

---

## Challenges

When trying to create the shaking row animation for an invaid guess, I had a lot of trouble trying to move the row back and forth. Initially I tried to use `.place()` to change the position of each tile in the guesses row, but because each row is in a grid, the entire grid of tiles would be displaced after any changes were made. To fix this I changed each tile's `padx` in the row and recursively called the `move()` function to create a shaking effect where the `padx` was changed in increments of 5. This created a smooth shaking effect that kept the grid intact and indicates an invalid guess to the user.

When I initially added the timing logic to change the color of a valid guess (left color is revealed before the right), I noticed that if I pressed the restart button before the tiles finished changing colors, the colored tiles would carry over into the next game. To fix this I added a loop to collect all the active `.after()` ids, and then canceled them all using `.after_cancel(<id>)`. This ensured that all tiles were properly reset for the next game.

---

## Technologies Used

- **Python 3**
- **Tkinter**

---

## How to Run

1. Clone this repository:

```bash
git clone https://github.com/yourusername/wordle-terminal
cd wordle-terminal
```

2. Compile and run

---

## Example

TBA
