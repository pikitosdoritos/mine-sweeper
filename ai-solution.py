import tkinter as tk
import random

SIZE = 10        # поле 10x10
MINES = 15       # количество мин

class Minesweeper:
    def __init__(self, root):
        self.root = root
        self.root.title("Minesweeper")

        self.first_click = True
        self.buttons = {}
        self.mines = set()
        self.flags = set()
        self.opened = set()

        self.frame = tk.Frame(root)
        self.frame.pack() 

        for r in range(SIZE):
            for c in range(SIZE):
                b = tk.Button(
                    self.frame, width=2, height=1,
                    command=lambda r=r, c=c: self.open(r, c)
                )
                b.bind("<Button-3>", lambda e, r=r, c=c: self.toggle_flag(r, c))
                b.grid(row=r, column=c)
                self.buttons[(r, c)] = b

    def place_mines(self, safe):
        cells = [(r, c) for r in range(SIZE) for c in range(SIZE) if (r, c) != safe]
        self.mines = set(random.sample(cells, MINES))

    def count_mines(self, r, c):
        return sum(
            (nr, nc) in self.mines
            for nr in range(r-1, r+2)
            for nc in range(c-1, c+2)
            if 0 <= nr < SIZE and 0 <= nc < SIZE
        )

    def open(self, r, c):
        if (r, c) in self.flags or (r, c) in self.opened:
            return

        if self.first_click:
            self.place_mines((r, c))
            self.first_click = False

        if (r, c) in self.mines:
            self.game_over(False)
            return

        self.reveal(r, c)

        if len(self.opened) == SIZE * SIZE - MINES:
            self.game_over(True)

    def reveal(self, r, c):
        if (r, c) in self.opened:
            return

        self.opened.add((r, c))
        btn = self.buttons[(r, c)]
        btn.config(relief=tk.SUNKEN, state=tk.DISABLED)

        mines = self.count_mines(r, c)
        if mines > 0:
            btn.config(text=str(mines))
        else:
            for nr in range(r-1, r+2):
                for nc in range(c-1, c+2):
                    if 0 <= nr < SIZE and 0 <= nc < SIZE:
                        self.reveal(nr, nc)

    def toggle_flag(self, r, c):
        if (r, c) in self.opened:
            return

        btn = self.buttons[(r, c)]
        if (r, c) in self.flags:
            self.flags.remove((r, c))
            btn.config(text="")
        else:
            self.flags.add((r, c))
            btn.config(text="🚩")

    def game_over(self, win):
        for (r, c), btn in self.buttons.items():
            if (r, c) in self.mines:
                btn.config(text="💣", bg="red")
            btn.config(state=tk.DISABLED)

        msg = "ПОБЕДА 🎉" if win else "ПРОИГРЫШ 💥"
        tk.messagebox.showinfo("Game Over", msg)

if __name__ == "__main__":
    root = tk.Tk()
    Minesweeper(root)
    root.mainloop()
