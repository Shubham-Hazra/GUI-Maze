import random
import time
from tkinter import BOTH, Canvas, Tk


class Point():
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y


class Line():
    def __init__(self, p1, p2) -> None:
        self.p1 = p1
        self.p2 = p2

    def draw(self, canvas, fill_color):
        canvas.create_line(
            self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=fill_color, width=2
        )


class Window():
    def __init__(self, width, height) -> None:
        self.root = Tk()
        self.root.title("GUI Maze")
        self.canvas = Canvas(self.root, height=height, width=width)
        self.canvas.pack()
        self.is_running = False
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.root.update_idletasks()
        self.root.update()

    def wait_for_close(self):
        self.is_running = True
        while self.is_running:
            self.redraw()

    def close(self):
        self.is_running = False


class Cell:
    def __init__(self, x1, y1, x2, y2, win):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.visited = False
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2
        self._win = win

    def draw(self):
        bg_color = "#d9d9d9"
        if self.has_left_wall:
            self._win.canvas.create_line(
                self._x1, self._y1, self._x1, self._y2, fill="black", width=2)
        else:
            self._win.canvas.create_line(
                self._x1, self._y1, self._x1, self._y2, fill=bg_color, width=2)

        if self.has_top_wall:
            self._win.canvas.create_line(
                self._x1, self._y1, self._x2, self._y1, fill="black", width=2)
        else:
            self._win.canvas.create_line(
                self._x1, self._y1, self._x2, self._y1, fill=bg_color, width=2)

        if self.has_right_wall:
            self._win.canvas.create_line(
                self._x2, self._y1, self._x2, self._y2, fill="black", width=2)
        else:
            self._win.canvas.create_line(
                self._x2, self._y1, self._x2, self._y2, fill=bg_color, width=2)

        if self.has_bottom_wall:
            self._win.canvas.create_line(
                self._x1, self._y2, self._x2, self._y2, fill="black", width=2)
        else:
            self._win.canvas.create_line(
                self._x1, self._y2, self._x2, self._y2, fill=bg_color, width=2)


class Maze:
    def __init__(
        self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win,
    ):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self._cells = []
        self._create_cells()

    def _create_cells(self):
        for j in range(self.num_rows):
            row = []
            for i in range(self.num_cols):
                x1 = self.x1 + i * self.cell_size_x
                y1 = self.y1 + j * self.cell_size_y
                x2 = x1 + self.cell_size_x
                y2 = y1 + self.cell_size_y
                cell = Cell(x1, y1, x2, y2, self.win)
                row.append(cell)
            self._cells.append(row)
        for j in range(self.num_rows):
            for i in range(self.num_cols):
                self._draw_cell(j, i)

    def _draw_cell(self, i, j):
        cell = self._cells[i][j]
        cell.draw()
        self._animate()

    def _animate(self):
        self.win.redraw()
        time.sleep(0.05)

    def _break_walls_r(self, i, j):
        current_cell = self._cells[i][j]
        current_cell.visited = True

        while True:
            directions = []
            if i > 0 and not self._cells[i - 1][j].visited:  # Up
                directions.append((-1, 0))
            if i < self.num_rows - 1 and not self._cells[i + 1][j].visited:
                directions.append((1, 0))
            if j > 0 and not self._cells[i][j - 1].visited:  # Left
                directions.append((0, -1))
            if j < self.num_cols - 1 and not self._cells[i][j + 1].visited:
                directions.append((0, 1))

            if not directions:
                self._draw_cell(i, j)
                return

            di, dj = random.choice(directions)

            if di == -1:
                current_cell.has_top_wall = False
                self._cells[i - 1][j].has_bottom_wall = False
            elif di == 1:
                current_cell.has_bottom_wall = False
                self._cells[i + 1][j].has_top_wall = False
            elif dj == -1:
                current_cell.has_left_wall = False
                self._cells[i][j - 1].has_right_wall = False
            elif dj == 1:
                current_cell.has_right_wall = False
                self._cells[i][j + 1].has_left_wall = False

            self._break_walls_r(i + di, j + dj)

    def generate_maze(self):
        self._break_walls_r(0, 0)

    def _reset_cells_visited(self):
        for row in self._cells:
            for cell in row:
                cell.visited = False

    def _solve_r(self, i, j):
        self._animate()
        current_cell = self._cells[i][j]
        current_cell.visited = True

        if i == self.num_rows - 1 and j == self.num_cols - 1:
            return True

        directions = [
            (-1, 0),  # Up
            (1, 0),   # Down
            (0, -1),  # Left
            (0, 1)    # Right
        ]
        for di, dj in directions:
            ni, nj = i + di, j + dj
            if 0 <= ni < self.num_rows and 0 <= nj < self.num_cols:
                next_cell = self._cells[ni][nj]

                if not next_cell.visited:
                    if di == -1 and not current_cell.has_top_wall:
                        self.win.canvas.create_line(
                            current_cell._x1 + self.cell_size_x // 2,
                            current_cell._y1 + self.cell_size_y // 2,
                            next_cell._x1 + self.cell_size_x // 2,
                            next_cell._y1 + self.cell_size_y // 2,
                            fill="blue", width=2)
                        if self._solve_r(ni, nj):
                            return True
                        self.win.canvas.create_line(
                            current_cell._x1 + self.cell_size_x // 2,
                            current_cell._y1 + self.cell_size_y // 2,
                            next_cell._x1 + self.cell_size_x // 2,
                            next_cell._y1 + self.cell_size_y // 2,
                            fill="red", width=2)
                    elif di == 1 and not current_cell.has_bottom_wall:
                        self.win.canvas.create_line(
                            current_cell._x1 + self.cell_size_x // 2,
                            current_cell._y1 + self.cell_size_y // 2,
                            next_cell._x1 + self.cell_size_x // 2,
                            next_cell._y1 + self.cell_size_y // 2,
                            fill="blue", width=2)
                        if self._solve_r(ni, nj):
                            return True
                        self.win.canvas.create_line(
                            current_cell._x1 + self.cell_size_x // 2,
                            current_cell._y1 + self.cell_size_y // 2,
                            next_cell._x1 + self.cell_size_x // 2,
                            next_cell._y1 + self.cell_size_y // 2,
                            fill="red", width=2)
                    elif dj == -1 and not current_cell.has_left_wall:
                        self.win.canvas.create_line(
                            current_cell._x1 + self.cell_size_x // 2,
                            current_cell._y1 + self.cell_size_y // 2,
                            next_cell._x1 + self.cell_size_x // 2,
                            next_cell._y1 + self.cell_size_y // 2,
                            fill="blue", width=2)
                        if self._solve_r(ni, nj):
                            return True
                        self.win.canvas.create_line(
                            current_cell._x1 + self.cell_size_x // 2,
                            current_cell._y1 + self.cell_size_y // 2,
                            next_cell._x1 + self.cell_size_x // 2,
                            next_cell._y1 + self.cell_size_y // 2,
                            fill="red", width=2)
                    elif dj == 1 and not current_cell.has_right_wall:
                        self.win.canvas.create_line(
                            current_cell._x1 + self.cell_size_x // 2,
                            current_cell._y1 + self.cell_size_y // 2,
                            next_cell._x1 + self.cell_size_x // 2,
                            next_cell._y1 + self.cell_size_y // 2,
                            fill="blue", width=2)
                        if self._solve_r(ni, nj):
                            return True
                        self.win.canvas.create_line(
                            current_cell._x1 + self.cell_size_x // 2,
                            current_cell._y1 + self.cell_size_y // 2,
                            next_cell._x1 + self.cell_size_x // 2,
                            next_cell._y1 + self.cell_size_y // 2,
                            fill="red", width=2)

        return False

    def solve(self):
        self._reset_cells_visited()
        return self._solve_r(0, 0)


if __name__ == '__main__':
    win = Window(800, 600)

    maze = Maze(
        x1=50, y1=50, num_rows=10, num_cols=14,
        cell_size_x=50, cell_size_y=50, win=win
    )

    maze.generate_maze()

    if maze.solve():
        print("Maze solved!")
    else:
        print("No solution found.")

    win.wait_for_close()
