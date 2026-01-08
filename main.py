import tkinter as tk

SIZE = 10

class MineSweeper:
    def __init__(self, root):
        self.root = root
        self.root.title("MineSweeper")
        self.buttons = {}
        self.flags = set()
        self.opened = set()
        self.mines = {(2, 5)}
        self.frame = tk.Frame(root)
        self.frame.pack()
        
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

    def open(self, r, c):
        if (r, c) in self.flags or (r, c) in self.opened:
            return

        self.opened.add((r, c))
        btn = self.buttons[(r, c)]
        btn.config(relief=tk.SUNKEN, state=tk.DISABLED)
        
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
            
    def reveal(self, r, c):
        btn = self.buttons[(r, c)]
        if (r, c) in self.mines:
            btn.config(text = "💣", bg = "red")
        else: 
            btn.config(text = str(self.count_mines(r, c)))

if __name__ == "__main__":
    root = tk.Tk()
    MineSweeper(root)
    root.mainloop()