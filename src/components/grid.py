import flet as ft
from src.puzzle_logic.crossword import Orientation
from src.puzzle_logic.puzzle_manager import PuzzleManager
from src.components.completed_message import completed_message_dialog
from src.misc.difficulty import Difficulty, DIFFICULTY_TO_COLOR
from src.misc.time_tracker import Timer
from src.misc.utils import generate_puzzle

CELL_SIZE = 40
ALL_CELLS = []

class Cell(ft.TextField):

    def __init__(self, puzzle, right_val, variable=None):
        super().__init__()
        self.height = CELL_SIZE
        self.width = CELL_SIZE
        self.text_align = "center"
        self.content_padding = 3
        self.text_size = 20
        self.border_color = "black"
        self.puzzle = puzzle
        self.puzzle.cells.append(self)
        ALL_CELLS.append(self)
        self.right_val = right_val
        if variable:
            self.label = variable
            self.label_style = ft.TextStyle(size=15, color="green", weight=ft.FontWeight.W_600)
        self.on_change = self.on_modify

    @staticmethod
    def check_if_done():
        pass

    def on_modify(self, event):
        if not event.control.value:
            self.border_color = "black"
            self.update()
            return
        try:
            num = event.control.value
            if num == self.right_val and all(cell.value == cell.right_val for cell in self.puzzle.cells):
                for cell in self.puzzle.cells:
                    if cell != self:
                        cell.border_color = "green"
                        cell.update()
                self.border_color = "green"
                self.update()
                Cell.check_if_done()
                return
            num = int(num)
            if len(str(num)) > 1: self.border_color = "red"
            else: self.border_color = "black"
        except ValueError:
            self.border_color = "red"
        self.update()

def grid_component(page: ft.Page, puzzle_manager: PuzzleManager, time_txt: ft.Text, timer: Timer) -> ft.Column:
    puzzles = puzzle_manager.puzzles
    variables = puzzle_manager.variables
    difficulty = puzzle_manager.difficulty
    crossword_grid = puzzle_manager.crossword_grid

    starting_points = {puzzles[variables[variable][0]].start: variable for variable in variables}
    cell_to_puzzle = {}
    for num in puzzles:
        puzzle = puzzles[num]
        puzzle.cells = []
        for i in range(len(num)):
            if puzzle.orientation == Orientation.LEFT_TO_RIGHT:
                cell_to_puzzle[(puzzle.start[0] + i, puzzle.start[1])] = puzzle
            else:
                cell_to_puzzle[(puzzle.start[0], puzzle.start[1] + i)] = puzzle

    def is_completed():
        if all(cell.value == cell.right_val for cell in ALL_CELLS):
            timer.stop()
            page.open(completed_message_dialog(page, difficulty, time_txt)) # NOQA

    Cell.check_if_done = is_completed

    def get_cell(y, x):
        val = crossword_grid.grid[y][x]
        if val == '.':
            return ft.Container(height=CELL_SIZE, width=CELL_SIZE)
        elif (x, y) in starting_points:
            return Cell(cell_to_puzzle[(x, y)], val, variable=starting_points[(x, y)])
        else:
            return Cell(cell_to_puzzle[(x, y)], val)

    return ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            ft.Row(spacing=10,
                   alignment=ft.MainAxisAlignment.CENTER,
                   controls=[
                       ft.Text("Difficulty:", size=20, weight=ft.FontWeight.W_600),
                       ft.Text(difficulty.name, size=20, color=DIFFICULTY_TO_COLOR[difficulty],
                               weight=ft.FontWeight.W_600),
                       timer,
                       time_txt
                   ]),
            ft.Container(height=20),
            ft.Row(
                spacing=0,
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Column(
                        spacing=0,
                        controls=[
                            ft.Container(height=5),
                            *[get_cell(j, i) for j in range(crossword_grid.height)]
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ) for i in range(crossword_grid.width)
                ],
                scroll=ft.ScrollMode.HIDDEN
            )
        ]
    )

if __name__ == "__main__":
    PUZZLE_MANAGER = generate_puzzle(Difficulty.MEDIUM, set(range(2, 11)))
    print(PUZZLE_MANAGER.variables)
    print(PUZZLE_MANAGER.crossword_grid.height, PUZZLE_MANAGER.crossword_grid.width)
    PUZZLE_MANAGER.crossword_grid.print_grid()
