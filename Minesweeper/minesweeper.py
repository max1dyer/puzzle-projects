import random
import tkinter as tk

# Define colors
APP_BG = "#F2F0E7"
BTN_BG1 = "#60B960"
BTN_BG2 = "#72C972"
BTN_BG_ACTIVE = "#87DC87"
BTN_BG1_DISABLED = "#E4DCC4"
BTN_BG2_DISABLED = "#ECE6D2"
RESTART_BG = "#ECE6D2"
HOVER_BG = "#D3CCB2"
MODE_BG = "#ECE6D2"
BG_MINES = ["#C62D2D", "#DB6A00", "#266D06", "#0077A5", "#1127CB", "#7A0CAD", "#AC00A1"]
BG_MINE_ACTIVE = "#B82222"
TEXT = "#000000"
TEXT_1 = "#4A5ADA"
TEXT_2 = "#09A12A"
TEXT_3 = "#BC3434"
TEXT_4 = "#8D23BF"
TEXT_5 = "#C97303"
TEXT_6 = "#D21BBF"
TEXT_7 = "#0B9CC8"
TEXT_8 = "#007007"
TEXT_COLORS = [TEXT_1, TEXT_2, TEXT_3, TEXT_4, TEXT_5, TEXT_6, TEXT_7, TEXT_8]

# Generate randomized minesweeper board
def generate_board(rows, cols, num_mines):
    # Create an empty board
    board = [[0 for _ in range(cols)] for _ in range(rows)]
    
    # Place mines randomly on the board
    mines_placed = 0
    while mines_placed < num_mines:
        r = random.randint(0, rows - 1)
        c = random.randint(0, cols - 1)
        if board[r][c] != 'M':  # Check if there's already a mine
            board[r][c] = 'M'
            mines_placed += 1
            
            # Update adjacent cells' counts
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if 0 <= r + i < rows and 0 <= c + j < cols and board[r + i][c + j] != 'M':
                        board[r + i][c + j] += 1
    
    return board

# Create the GUI for the minesweeper game
class MinesweeperGUI:
    def __init__(self, root:tk.Tk, rows, cols, num_mines):
        self.root = root
        self.root.title("Minesweeper")
        self.root.configure(bg=APP_BG, padx=10, pady=10)
        self.root.resizable(False, False)

        self.board = generate_board(rows, cols, num_mines)
        self.buttons = [[None for _ in range(cols)] for _ in range(rows)]
        self.rows = rows
        self.cols = cols
        self.num_mines = num_mines
        self.mines_marked = 0
        self.cells_revealed = 0
        self.mode = True  # True for normal mode, False for adding mines mode
        self.games_won = 0
        self.game_over = False

        self.popup = None
        self.popup_id = None

        self.build_widgets()
        self.root.focus_force()

    def build_widgets(self):
        # Create the minefield grid
        self.board_frame = tk.Frame(self.root, bg=APP_BG)
        self.board_frame.pack(padx=18, pady=(4, 18))

        # Create the grid of buttons
        for r in range(self.rows):
            for c in range(self.cols):
                btn = tk.Button(
                    self.board_frame, 
                    width=3, height=1, 
                    bg = BTN_BG1 if (r + c) % 2 == 0 else BTN_BG2,
                    activebackground = BTN_BG_ACTIVE,
                    relief='flat', bd = 0,
                    command=lambda r=r, c=c: self.reveal_cell(r, c) if self.mode else self.mark_mine(r, c))
                btn.grid(row=r, column=c)
                self.buttons[r][c] = btn

        controls = tk.Frame(self.root, bg=APP_BG)
        controls.pack(pady=(0, 10))

        self.restart_btn = tk.Button(
            controls,
            text="Restart",
            font=("Arial", 12, "bold"),
            command=self.restart_game,
            bg=RESTART_BG,
            fg=TEXT,
            activebackground=HOVER_BG,
            relief="raised",
            bd=1,
            padx=12,
            pady=4
        )
        self.restart_btn.grid(row=0, column=0, padx=(0, 10))

        # Create a button to toggle between normal mode (revealing cells) and marking mode (marking mines), with dynamic text that updates based on the current mode
        self.mode_btn = tk.Button(
            controls,
            text="Mark Mines" if self.mode else "Reveal Cells",
            font=("Arial", 12, "bold"),
            command=self.change_mode,
            bg=RESTART_BG,
            fg=TEXT,
            activebackground=HOVER_BG,
            disabledforeground=TEXT,
            relief="raised",
            bd=1,
            padx=12,
            pady=4
        )
        self.mode_btn.grid(row=0, column=1, padx=(0, 10))

        # Display the number of mines remaining to be marked, updating dynamically as mines are marked or unmarked
        self.mine_label = tk.Label(
            controls,
            text=f"Mines: {self.num_mines - self.mines_marked}",
            font=("Arial", 12),
            bg=APP_BG,
            fg=TEXT
        )
        self.mine_label.grid(row=0, column=2, padx=(0, 10))

        # Display the number of games won, updating dynamically when the player wins a game
        self.games_won_label = tk.Label(
            controls,
            text=f"Games Won: {self.games_won}",
            font=("Arial", 12),
            bg=APP_BG,
            fg=TEXT
        )
        self.games_won_label.grid(row=0, column=3, padx=(0, 10))

    # Reveal the cell at (r, c) and recursively reveal adjacent cells if it's empty
    def reveal_cell(self, r, c):
        # If the cell is already revealed or marked, do nothing
        if self.buttons[r][c]['text'] == 'X' or self.buttons[r][c]['state'] == 'disabled' or self.game_over:
            return
        
        # If the cell contains a mine, reveal the board and end the game
        if self.board[r][c] == 'M':
            self.buttons[r][c].config(text='💣', bg=BG_MINES[0], font=('Arial', 9, 'bold'), state='disabled', disabledforeground=TEXT)
            self.reveal_board(r, c)
            self.mode_btn.config(state='disabled')
            self.show_popup("Oh no! You blew up!", 3000)
            self.game_over = True 
        # If the cell is a number, reveal it and disable the button
        elif self.board[r][c] != 'M' and self.buttons[r][c]['text'] != 'X':
            self.cells_revealed += 1
            self.buttons[r][c].config(bg=BTN_BG1_DISABLED if (r + c) % 2 == 0 else BTN_BG2_DISABLED, state='disabled', disabledforeground=TEXT)
            
            # If the cell is empty, recursively reveal adjacent cells
            if self.board[r][c] == 0:
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if 0 <= r + i < len(self.board) and 0 <= c + j < len(self.board[0]):
                            self.reveal_cell(r + i, c + j)
            # Only if the cell is a number greater than 0, reveal the number
            else:
                self.buttons[r][c].config(text=str(self.board[r][c]), disabledforeground = TEXT_COLORS[int(self.board[r][c] - 1)], font=('Arial', 9, 'bold'))

            if self.cells_revealed == self.rows * self.cols - self.num_mines:
                self.mode_btn.config(state='disabled')
                self.show_popup("Congratulations! You won!", 3000)
                self.restart_btn.config(text="Play Again")
                self.games_won += 1
                self.games_won_label.config(text=f"Games Won: {self.games_won}")
                self.game_over = True

    # Mark or unmark a mine at (r, c) based on the current mode
    def mark_mine(self, r, c):
        # If the cell is already revealed or the game is over, do nothing
        if self.buttons[r][c]['state'] == 'disabled' or self.game_over:
            return
        # If the cell is not marked, mark it as a mine; if it's already marked, unmark it
        if self.buttons[r][c]['text'] != 'X' and self.buttons[r][c]['state'] == 'normal':
            self.buttons[r][c].config(text='X', font=('Arial', 9, 'bold'), fg=TEXT)
            self.mines_marked += 1
            self.mine_label.config(text=f"Mines: {self.num_mines - self.mines_marked}")
        elif self.buttons[r][c]['text'] == 'X':
            self.buttons[r][c].config(text='')
            self.mines_marked -= 1
            self.mine_label.config(text=f"Mines: {self.num_mines - self.mines_marked}")

    # Reveal all mines on the board with a random delay to create a dynamic effect when the game is over
    def reveal_board(self, row, col):
        mines = []
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] == 'M' and (r, c) != (row, col):
                    mines.append((r, c))
        # Shuffle the list of mines to reveal them in random order
        random.shuffle(mines) 
        for r, c in mines:
            # Reveal each mine with a random delay to create a dynamic effect
            self.root.after(random.randint(200, 3000), lambda r=r, c=c: self.buttons[r][c].config(text='💣', bg=random.choice(BG_MINES), font=('Arial', 9, 'bold'), state='disabled', disabledforeground=TEXT))

    # Show a popup message with the specified text, geometry, and duration, and ensure that only one popup is shown at a time
    def show_popup(self, message, duration):
        if self.popup is not None:
            self.popup.destroy()
            self.popup = None

        # Cancel any existing popup timer to prevent multiple popups from stacking
        if self.popup_id is not None:
            self.root.after_cancel(self.popup_id)
            self.popup_id = None

        self.popup = tk.Toplevel(self.root)
        self.popup.overrideredirect(True)
        self.popup.configure(bg=APP_BG)

        label = tk.Label(
            self.popup, 
            text=message, 
            font=("Arial", 11, "bold"), 
            bd=1,
            padx=10,
            pady=5,
            bg=APP_BG, 
            fg=TEXT)
        label.pack()

        self.popup.update_idletasks()
        # Center the popup horizontally relative to the main window and position it just below the title
        root_x = self.root.winfo_rootx()
        root_y = self.root.winfo_rooty()
        root_w = self.root.winfo_width()
        popup_w = self.popup.winfo_width()
        x = root_x + (root_w - popup_w) // 2
        y = root_y + 78
        self.popup.geometry(f"+{x}+{y}")

        # Close the popup after the specified duration
        self.popup_id = self.root.after(duration, self.hide_popup)

    # Destroy the popup window and reset the popup state variables
    def hide_popup(self):
        if self.popup is not None:
            self.popup.destroy()
            self.popup = None
        self.popup_id = None

    # Restart the game by generating a new board and resetting all buttons and game state
    def restart_game(self):
        self.board = generate_board(self.rows, self.cols, self.num_mines)
        self.mines_marked = 0
        self.game_over = False
        self.mode = True
        self.mode_btn.config(text="Mark Mines", state='normal')
        self.mine_label.config(text=f"Mines: {self.num_mines - self.mines_marked}")
        self.hide_popup()
        self.cells_revealed = 0
        self.restart_btn.config(text="Restart")

        # Cancel any pending mine reveals to prevent them from affecting the new game
        ids = self.root.after_info()
        for id in ids:
            self.root.after_cancel(id)

        for r in range(self.rows):
            for c in range(self.cols):
                self.buttons[r][c].config(text='', bg=BTN_BG1 if (r + c) % 2 == 0 else BTN_BG2, activebackground=BTN_BG_ACTIVE, state='normal', disabledforeground=TEXT)
    
    # Toggle between normal mode (revealing cells) and marking mode (marking mines)
    def change_mode(self):
        self.mode = not self.mode
        self.mode_btn.config(text="Mark Mines" if self.mode else "Reveal Cells")

if __name__ == "__main__":
    root = tk.Tk()
    app = MinesweeperGUI(root, 14, 18, 40)
    root.mainloop()