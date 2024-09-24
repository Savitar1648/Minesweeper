import tkinter as tk
from tkinter import messagebox
import random

class MinesweeperGUI:
    def __init__(self, master, size=10, num_mines=15):
        self.master = master
        self.size = size
        self.num_mines = num_mines
        self.buttons = [[None for _ in range(size)] for _ in range(size)]
        self.mine_locations = []
        self.revealed = [[False for _ in range(size)] for _ in range(size)]
        self.game_over = False

        self.create_widgets()
        self.generate_mines()

        
        self.master.update_idletasks()
        width = self.master.winfo_width()
        height = self.master.winfo_height()
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.master.geometry(f"{width}x{height}+{x}+{y}")
        self.master.title("Minesweeper")

    def create_widgets(self):
        for row in range(self.size):
            for col in range(self.size):
                button = tk.Button(self.master, width=4, height=2, font=("Arial", 16, "bold"), bg="#B0C4DE",
                                   command=lambda r=row, c=col: self.on_click(r, c))
                button.grid(row=row, column=col, padx=2, pady=2)
                self.buttons[row][col] = button

    def generate_mines(self):
        mines = 0
        while mines < self.num_mines:
            row = random.randint(0, self.size - 1)
            col = random.randint(0, self.size - 1)
            if (row, col) not in self.mine_locations:
                self.mine_locations.append((row, col))
                mines += 1

    def count_adjacent_mines(self, row, col):
        mine_count = 0
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if 0 <= r < self.size and 0 <= c < self.size:
                    if (r, c) in self.mine_locations:
                        mine_count += 1
        return mine_count

    def on_click(self, row, col):
        if self.game_over or self.revealed[row][col]:
            return

        if (row, col) in self.mine_locations:
            self.buttons[row][col].config(text='M', bg='red', fg='white')
            self.game_over = True
            self.end_game("Hai perso!")
        else:
            adjacent_mines = self.count_adjacent_mines(row, col)
            self.buttons[row][col].config(text=str(adjacent_mines), state="disabled", relief=tk.SUNKEN,
                                          bg='#F0F8FF', fg='#00008B')
            self.revealed[row][col] = True

            if adjacent_mines == 0:
                self.buttons[row][col].config(text='', bg='#D3D3D3')
                for r in range(row - 1, row + 2):
                    for c in range(col - 1, col + 2):
                        if 0 <= r < self.size and 0 <= c < self.size:
                            if not self.revealed[r][c]:
                                self.on_click(r, c)

            if self.check_victory():
                self.end_game("Hai vinto!")

    def check_victory(self):
        for row in range(self.size):
            for col in range(self.size):
                if (row, col) not in self.mine_locations and not self.revealed[row][col]:
                    return False
        return True

    def end_game(self, message):
        for row in range(self.size):
            for col in range(self.size):
                if (row, col) in self.mine_locations:
                    self.buttons[row][col].config(text='M', bg='red', fg='white')
        messagebox.showinfo("Fine del gioco", message)

class MinesweeperApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Minesweeper")
        

        self.menu_frame = tk.Frame(self.master)
        self.menu_frame.pack(expand=True)

      
        self.title_label = tk.Label(self.menu_frame, text="Minesweeper", font=("Arial", 24, "bold"))
        self.title_label.pack(pady=10)

      
        self.subtitle_label = tk.Label(self.menu_frame, text="by GretaThunberg, fatto in Python", font=("Arial", 14))
        self.subtitle_label.pack(pady=5)

        
        self.play_button = tk.Button(self.menu_frame, text="Gioca", font=("Arial", 18), command=self.start_game)
        self.play_button.pack(pady=20)

    def start_game(self):
       
        self.menu_frame.pack_forget()

        
        self.game = MinesweeperGUI(self.master, size=10, num_mines=15)

if __name__ == "__main__":
    root = tk.Tk()
    app = MinesweeperApp(root)
    root.mainloop()
