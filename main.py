from tkinter import messagebox
import tkinter as tk
import random

SIZE = 10
MINES = 15

class MineSweeper:
    def __init__(self, root):
        self.root = root
        self.root.title("MineSweeper")
        self.buttons = {}
        self.flags = set()
        self.opened = set()
        self.mines = set()
        self.frame = tk.Frame(root)
        self.frame.pack()
        self.first_click = True
        
        for r in range(SIZE):
            for c in range(SIZE):
                b = tk.Button(
                    self.frame, width = 2, height = 1,
                    command = lambda r=r, c=c: self.open(r, c)
                )
                b.bind("<Button-3>", lambda e, r=r, c=c: self.toggle_flag(r, c))
                b.grid(row=r, column=c)
                self.buttons[(r, c)] = b
                
    def count_mines(self, r, c):
        count = 0
        
        count += (r - 1, c - 1) in self.mines
        count += (r - 1, c) in self.mines
        count += (r - 1, c + 1) in self.mines
        count += (r, c - 1) in self.mines
        count += (r, c + 1) in self.mines
        count += (r + 1, c - 1) in self.mines
        count += (r + 1, c) in self.mines
        count += (r + 1, c + 1) in self.mines
        
        return count

    def place_mines(self, r, c):
        cells = []
        
        for nr in range(SIZE):
            for nc in range(SIZE):
                if (nr, nc) != (r, c):
                    cells.append((nr, nc))
                    
        self.mines.update(random.sample(cells, MINES))
        
    def open(self, r, c):
        if (r, c) in self.flags or (r, c) in self.opened:
            return

        self.opened.add((r, c))
        btn = self.buttons[(r, c)]
        btn.config(relief=tk.SUNKEN, state=tk.DISABLED)
        
        if self.first_click:
            self.place_mines(r, c)
            self.first_click = False
            
        self.reveal(r, c)
    
    def toggle_flag(self, r, c):
        if (r, c) in self.opened:
            return
        
        btn = self.buttons[(r, c)]        

        if (r, c) in self.flags:
            self.flags.remove((r, c))
            btn.config(text = "")
        else:
            self.flags.add((r, c))
            btn.config(text = "🚩")
            
    def open_cells_around_empty(self, r, c):
        neighbours = [
            (r - 1, c - 1),
            (r - 1, c),
            (r - 1, c + 1),
            (r, c - 1),
            (r, c + 1),
            (r + 1, c - 1),
            (r + 1, c),
            (r + 1, c + 1),
        ]

        for coords in neighbours:
            if coords in self.buttons and coords not in self.opened:
                self.open(*coords)
            
    def reveal(self, r, c):
        btn = self.buttons[(r, c)]
        value = self.count_mines(r, c) or ""
        
        if (r, c) in self.mines:
            self.game_over(win=False)
            return
        elif value == "":
            self.open_cells_around_empty(r, c)
        elif len(self.opened) == SIZE * SIZE - MINES:
            self.game_over(win=True)
            return
        else: 
            btn.config(text = str(value))
            
    def game_over(self, win):
        color = "green" if win else "red"
        for coords in self.mines:
            if coords in self.buttons:
                self.buttons[coords].config(text="💣", bg=color)
                
        for btn in self.buttons.values():
            btn.config(state=tk.DISABLED)
            
        msg = "WIN 🎉" if win else "LOSS 💥"
        messagebox.showinfo("Game Over", msg)

if __name__ == "__main__":
    root = tk.Tk()
    MineSweeper(root)
    root.mainloop()