import random
import tkinter as tk

# Hard coded colors for the application
GREEN = "#4ea646"
YELLOW = "#ffe057"
GRAY = "#929292"
TEXT = "#1b1b1b"
TEXT_GREEN = "#ffffff"
APP_BG = "#ededed"
TILE_BG = "#ffffff"
KEY_BG = "#ffffff"
HOVER_BG = "#dcdcdc"
HOVER_BG_GREEN = "#428b3c"
HOVER_BG_YELLOW = "#d8b648"
HOVER_BG_GRAY = "#696969"

class WordleGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Wordle")
        self.root.configure(bg=APP_BG, padx=10, pady=10)
        self.root.resizable(False, False)

        self.words = self.get_words_from_file("wordle_words.txt")
        self.answer = random.choice(self.words)
        self.curr_row = 0
        self.curr_col = 0
        self.game_over = False

        self.tiles = []
        self.keys = {}

        self.build_widgets()
        # Bind physical keyboard events
        self.root.bind("<Key>", self.handle_physical_key)
        self.root.focus_force()

    def build_widgets(self):
        title = tk.Label(
            self.root,
            text="WORDLE",
            font=("Arial", 30, "bold"),
            bg=APP_BG,
            fg=TEXT,
            pady=4
        )
        title.pack()

        # Add basic padding around the board
        self.board_frame = tk.Frame(self.root, bg=APP_BG)
        self.board_frame.pack(padx=18, pady=(4, 18))

        # Create the grid of tiles
        for i in range(6):
            row = []
            
            for j in range(5):
                tile = tk.Label(
                    self.board_frame, 
                    text="", 
                    width=4, 
                    height=2, 
                    font=("Arial", 24, "bold"),
                    borderwidth=2, 
                    relief="solid", 
                    bg=TILE_BG,
                    fg=TEXT)
                tile.grid(row=i, column=j, padx=5, pady=5)
                row.append(tile)
            self.tiles.append(row)

        controls = tk.Frame(self.root, bg=APP_BG)
        controls.pack(pady=(0, 10))

        restart_btn = tk.Button(
            controls,
            text="Restart",
            font=("Arial", 12, "bold"),
            command=self.restart_game,
            bg=KEY_BG,
            fg=TEXT,
            activebackground=HOVER_BG,
            relief="raised",
            bd=1,
            padx=12,
            pady=4
        )
        restart_btn.pack()

        # Create the on-screen keyboard
        self.keyboard_frame = tk.Frame(self.root, bg=APP_BG)
        self.keyboard_frame.pack(padx=10, pady=(8, 18))

        keyboard_rows = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
                        ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
                        ["ENTER", "Z", "X", "C", "V", "B", "N", "M", "⌫"]]
        
        for row in keyboard_rows:
            row_frame = tk.Frame(self.keyboard_frame, bg=APP_BG)
            row_frame.pack(pady=4)

            for key in row:
                width = 6 if key in ("ENTER", "⌫") else 3
                key_widget = tk.Button(
                    row_frame,
                    text=key,
                    width=width,
                    height=1,
                    font=("Arial", 12, "bold"),
                    bg=KEY_BG,
                    fg=TEXT,
                    activebackground=HOVER_BG,
                    activeforeground=TEXT,
                    relief="raised",
                    bd=2,
                    command=lambda k=key: self.handle_virtual_key(k))
                key_widget.pack(side="left", padx=3)
                if len(key) == 1 and key.isalpha():
                    self.keys[key] = key_widget

    # Load valid 5-letter words from the specified file
    def get_words_from_file(self, filename):
        with open(filename, "r") as f:
            # Only include lines that are exactly 5 letters long and contain only alphabetic characters
            words = [line.strip().lower() for line in f if len(line.strip()) == 5 and line.strip().isalpha()]
        return words
    
    # Handle physical keyboard events for ENTER, BACKSPACE, and letter keys
    def handle_physical_key(self, event):
        if self.game_over:
            return

        # Use keysym for special keys and char for regular characters
        key = event.keysym

        if key == "Return":
            self.submit_guess()
        elif key == "BackSpace":
            self.delete_letter()
        # Check if it's a single character and an alphabet letter, else we don't want to add it
        elif len(event.char) == 1 and event.char.isalpha():
            self.add_letter(event.char.upper())

    # Handle on-screen key presses for ENTER, BACKSPACE, and letter keys
    def handle_virtual_key(self, key: str):
        if self.game_over:
            return

        # Handle virtual key presses for ENTER, BACKSPACE, and letter keys
        if key == "ENTER":
            self.submit_guess()
        elif key == "⌫":
            self.delete_letter()
        else:
            self.add_letter(key)

    # Add a letter to the current guess and update the corresponding tile
    def add_letter(self, letter: str):
        if self.curr_col < 5 and self.curr_row < 6:
            self.tiles[self.curr_row][self.curr_col].config(text=letter)
            self.curr_col += 1

    # Remove the last letter from the current guess and update the tile
    def delete_letter(self):
        if self.curr_col > 0 and self.curr_row < 6:
            self.curr_col -= 1
            self.tiles[self.curr_row][self.curr_col].config(text="")

    # Check if the current guess is valid, color the tiles accordingly, and check for win/loss conditions
    def submit_guess(self):
        if self.game_over:
            return
        
        if self.curr_col != 5:
            return  # Not enough letters, add popup

        guess = "".join(self.tiles[self.curr_row][j].cget("text") for j in range(5)).lower()
        if guess not in self.words:
            return  # Invalid word, add popup
        self.color_tiles(guess)

        if guess == self.answer:
            self.game_over = True # add popup
        else:
            self.curr_row += 1
            self.curr_col = 0
            if self.curr_row == 6:
                self.game_over = True # add popup

    # Color the tiles and update the keyboard based on the guess and the answer
    def color_tiles(self, guess):
        # Count the number of each letter in the answer
        num_letters = {}
        for letter in self.answer:
            if letter in num_letters:
                num_letters[letter] += 1
            else:
                num_letters[letter] = 1

        # First pass: color green and count down letters
        for j in range(5):
            if self.answer[j] == guess[j]:
                self.tiles[self.curr_row][j].config(bg=GREEN, fg=TEXT_GREEN)
                self.keys[guess[j].upper()].config(bg=GREEN, fg=TEXT_GREEN, activebackground=HOVER_BG_GREEN, activeforeground=TEXT_GREEN)
                num_letters[guess[j]] -= 1
        
        # Second pass: color yellow and gray for remaining letters
        for j in range(5):
            tile = self.tiles[self.curr_row][j]
            key = self.keys[guess[j].upper()]

            # If the tile is already green, skip it so we don't overwrite the color of tile or keyboard
            if tile.cget("bg") == GREEN:
                continue
            elif guess[j] in self.answer and num_letters.get(guess[j], 0) > 0:
                tile.config(bg=YELLOW)
                num_letters[guess[j]] -= 1
                # Only update the key color to yellow if it hasn't already been colored green
                if key.cget("bg") != GREEN:
                    key.config(bg=YELLOW, activebackground=HOVER_BG_YELLOW)
            else:
                tile.config(bg=GRAY)
                # Only update the key color to gray if it hasn't already been colored green or yellow
                if key.cget("bg") not in (GREEN, YELLOW):
                    key.config(bg=GRAY, activebackground=HOVER_BG_GRAY)

    # Reset the game state and UI elements to start a new game
    def restart_game(self):
        self.answer = random.choice(self.words)
        self.curr_row = 0
        self.curr_col = 0
        self.game_over = False

        for r in range(6):
            for c in range(5):
                self.tiles[r][c].config(text="", bg=TILE_BG, fg=TEXT)

        for btn in self.keys.values():
            btn.config(bg=KEY_BG, activebackground=HOVER_BG, fg=TEXT, activeforeground=TEXT)

if __name__ == "__main__":
    root = tk.Tk()
    app = WordleGUI(root)
    root.mainloop()