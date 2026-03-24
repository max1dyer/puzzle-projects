import random
import tkinter as tk

class WordleGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Wordle")
        self.root.configure(bg="white")
        self.root.resizable(False, False)

        self.words = self.get_words_from_file("wordle_words.txt")
        self.answer = random.choice(self.words)
        self.curr_row = 0
        self.curr_col = 0
        self.game_over = False

        self.tiles = []
        self.keys = {}

        self.build_widgets()
        self.root.focus_force()

    def build_widgets(self):
        # Create the grid of tiles
        for i in range(6):
            row = []
            for j in range(5):
                tile = tk.Label(
                    self.root, 
                    text="", 
                    width=4, 
                    height=2, 
                    font=("Helvetica", 24),
                    borderwidth=2, 
                    relief="solid", 
                    bg="white")
                tile.grid(row=i, column=j, padx=5, pady=5)
                row.append(tile)
            self.tiles.append(row)

        # Create the on-screen keyboard
        self.keyboard_frame = tk.Frame(self.root, bg="white")
        self.keyboard_frame.grid(row=6, column=0, columnspan=5, pady=10)

        keyboard_rows = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
                        ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
                        ["ENTER", "Z", "X", "C", "V", "B", "N", "M", "⌫"]]
        for row in keyboard_rows:
            row_frame = tk.Frame(self.keyboard_frame, bg="white")
            row_frame.pack(pady=3)
            for key in row:
                width = 6 if key in ("ENTER", "⌫") else 3
                btn = tk.Button(
                    row_frame,
                    text=key,
                    width=width,
                    height=1,
                    font=("Arial", 12, "bold"),
                    bg="white",
                    fg="black",
                    activebackground="white",
                    activeforeground="black",
                    relief="raised",
                    bd=2,
                    command=lambda k=key: self.handle_virtual_key(k))
                btn.pack(side="left", padx=2)
                if len(key) == 1 and key.isalpha():
                    self.keys[key] = btn

    def get_words_from_file(self, filename):
        with open(filename, "r") as f:
            # Only include lines that are exactly 5 letters long and contain only alphabetic characters
            words = [line.strip().lower() for line in f if len(line.strip()) == 5 and line.strip().isalpha()]
        return words
    
    def handle_virtual_key(self, key: str):
        if self.game_over:
            return

        self.root.focus_force()

        if key == "ENTER":
            self.submit_guess()
        elif key == "⌫":
            self.delete_letter()
        else:
            self.add_letter(key)

    def add_letter(self, letter: str):
        if self.curr_col < 5 and self.curr_row < 6:
            self.tiles[self.curr_row][self.curr_col].config(text=letter)
            self.curr_col += 1

    def delete_letter(self):
        if self.curr_col > 0 and self.curr_row < 6:
            self.curr_col -= 1
            self.tiles[self.curr_row][self.curr_col].config(text="")

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

    def color_tiles(self, guess):
        num_letters = {}
        for letter in self.answer:
            if letter in num_letters:
                num_letters[letter] += 1
            else:
                num_letters[letter] = 1

        for j in range(5):
            if self.answer[j] == guess[j]:
                self.tiles[self.curr_row][j].config(bg="green", fg="white")
                self.keys[guess[j].upper()].config(bg="green", fg="white")
                num_letters[guess[j]] -= 1
        
        for j in range(5):
            if self.tiles[self.curr_row][j].cget("bg") == "green":
                continue
            elif guess[j] in self.answer and num_letters.get(guess[j], 0) > 0:
                self.tiles[self.curr_row][j].config(bg="yellow", fg="black")
                num_letters[guess[j]] -= 1
                if self.keys[guess[j].upper()].cget("bg") != "green":
                    self.keys[guess[j].upper()].config(bg="yellow", fg="black")
            else:
                self.tiles[self.curr_row][j].config(bg="light gray", fg="black")
                if self.keys[guess[j].upper()].cget("bg") not in ("green", "yellow"):
                    self.keys[guess[j].upper()].config(bg="light gray", fg="black")

if __name__ == "__main__":
    root = tk.Tk()
    app = WordleGUI(root)
    root.mainloop()