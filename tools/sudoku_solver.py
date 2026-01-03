import tkinter as tk
from tkinter import messagebox

class SudokuUI:
    def __init__(self, master):
        self.master = master
        master.title("Sudoku Solver")

        self.cells = {}
        self.grid_frame = tk.Frame(master)
        self.grid_frame.pack(pady=10)

        for i in range(9):
            for j in range(9):
                entry = tk.Entry(self.grid_frame, width=3, font=('Arial', 18), justify='center')
                entry.grid(row=i, column=j, padx=1, pady=1)
                self.cells[(i, j)] = entry
                # Add thicker lines for 3x3 subgrids
                if (i % 3 == 2 and i < 8) or (j % 3 == 2 and j < 8):
                    if (i % 3 == 2 and i < 8) and (j % 3 == 2 and j < 8):
                         tk.Frame(self.grid_frame, height=2, width=entry.winfo_reqwidth()*9 + 18, bg='black').grid(row=i, column=0, columnspan=9, sticky='s', pady=(0,2))
                         tk.Frame(self.grid_frame, width=2, height=entry.winfo_reqheight()*9 + 18, bg='black').grid(row=0, column=j, rowspan=9, sticky='e', padx=(0,2))
                    elif (i % 3 == 2 and i < 8):
                        tk.Frame(self.grid_frame, height=2, width=entry.winfo_reqwidth()*9 + 18, bg='black').grid(row=i, column=0, columnspan=9, sticky='s', pady=(0,2))
                    elif (j % 3 == 2 and j < 8):
                         tk.Frame(self.grid_frame, width=2, height=entry.winfo_reqheight()*9 + 18, bg='black').grid(row=0, column=j, rowspan=9, sticky='e', padx=(0,2))


        self.solve_button = tk.Button(master, text="Solve", command=self.solve_sudoku)
        self.solve_button.pack(pady=5)

        self.clear_button = tk.Button(master, text="Clear", command=self.clear_grid)
        self.clear_button.pack(pady=5)

    def get_grid(self):
        grid = []
        for i in range(9):
            row = []
            for j in range(9):
                val = self.cells[(i, j)].get()
                if val.isdigit() and 1 <= int(val) <= 9:
                    row.append(int(val))
                else:
                    row.append(0) # 0 for empty cells
            grid.append(row)
        return grid

    def set_grid(self, grid):
        for i in range(9):
            for j in range(9):
                self.cells[(i, j)].delete(0, tk.END)
                if grid[i][j] != 0:
                    self.cells[(i, j)].insert(0, str(grid[i][j]))

    def solve_sudoku(self):
        grid = self.get_grid()
        # Placeholder for advanced Sudoku solving logic
        # For example, using backtracking, constraint propagation, etc.
        if self.solve_logic(grid):
            self.set_grid(grid)
            if self.is_solution_valid(grid):
                messagebox.showinfo("Success", "Sudoku Solved!")
            else:
                messagebox.showerror("Error", "Solution is invalid after re-check!")
        else:
            messagebox.showerror("Error", "Could not solve Sudoku or input is invalid.")

    def solve_logic(self, grid):
        # --- ADVANCED SOLVING TECHNIQUES GO HERE ---
        # Example: Backtracking (simplistic version)
        find = self.find_empty(grid)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if self.is_valid_move(grid, i, (row, col)):
                grid[row][col] = i
                if self.solve_logic(grid):
                    return True
                grid[row][col] = 0 # Backtrack
        return False
        # --- END OF SOLVING LOGIC PLACEHOLDER ---

    def find_empty(self, grid):
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    return (i, j)
        return None

    def is_valid_move(self, grid, num, pos):
        # Check row
        for i in range(9):
            if grid[pos[0]][i] == num and pos[1] != i:
                return False
        # Check column
        for i in range(9):
            if grid[i][pos[1]] == num and pos[0] != i:
                return False
        # Check 3x3 box
        box_x = pos[1] // 3
        box_y = pos[0] // 3
        for i in range(box_y*3, box_y*3 + 3):
            for j in range(box_x*3, box_x*3 + 3):
                if grid[i][j] == num and (i,j) != pos:
                    return False
        return True

    def is_solution_valid(self, grid):
        # Error proofing: Re-check the entire solved grid
        for r in range(9):
            for c in range(9):
                num = grid[r][c]
                if num == 0: return False # Must be filled
                # Temporarily set to 0 to check validity against others
                grid[r][c] = 0
                if not self.is_valid_move(grid, num, (r, c)):
                    grid[r][c] = num # Restore
                    return False
                grid[r][c] = num # Restore
        return True

    def clear_grid(self):
        for i in range(9):
            for j in range(9):
                self.cells[(i, j)].delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuUI(root)
    root.mainloop()