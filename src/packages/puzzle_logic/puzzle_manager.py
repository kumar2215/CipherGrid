from packages.problem_generation.generate import MathProblem
from packages.misc.difficulty import Difficulty
from packages.puzzle_logic.crossword import CrossWordPuzzle, create_crossword_grid
import sympy as sp
import re
import random
from dataclasses import dataclass
import multiprocessing

@dataclass
class PuzzleParameters:

    num_of_variables: int
    complexity: int
    max_level: int
    min_length: int
    max_length: int
    RHS_range: tuple[int, ...]

def convert_base(num: int, base: int) -> str:
    if num == 0: return "0"
    digits = []
    while num:
        digits.append(str(num % base))
        num //= base
    return "".join(digits[::-1])

class PuzzleManager:

    def __init__(self, difficulty: Difficulty, bases: set[int], queue):
        self.difficulty = difficulty
        self.bases = bases
        self.puzzle_params = None
        match self.difficulty:
            case Difficulty.EASY:
                self.puzzle_params = PuzzleParameters(6, 8, 2, 4, 6, tuple(map(int, (-1e2, 1e2))))
            case Difficulty.MEDIUM:
                self.puzzle_params = PuzzleParameters(7, 10, 3, 5, 7, tuple(map(int, (-1e3, 1e3))))
            case Difficulty.HARD:
                self.puzzle_params = PuzzleParameters(8, 12, 4, 6, 8, tuple(map(int, (-1e4, 1e4))))
        self.variables = [0] * self.puzzle_params.num_of_variables
        self.hints = {}
        self.gen = MathProblem(self.puzzle_params.max_level)
        i = 0
        LEN_LIMIT = 100
        temp_bases = self.bases.copy()
        while i < self.puzzle_params.num_of_variables:
            var = chr(i+97)
            target = sp.Integer(random.randint(*self.puzzle_params.RHS_range))
            expr, sol = self.gen.generate(self.puzzle_params.complexity, sp.Symbol(var), target)
            if (expr, sol) == (None, None): continue
            try:
                expr_len = len(sp.latex(expr))
                sol_len = len(sp.latex(sol))
                if expr_len >= LEN_LIMIT or sol_len >= LEN_LIMIT: continue
                sol_str = sp.latex(sp.simplify(sol))
                nums = re.findall(r"\d+", sol_str)
                if any(len(num) >= 2 * self.puzzle_params.min_length for num in nums): continue
            except Exception as e: # NOQA
                continue
            if not temp_bases: temp_bases = self.bases.copy()
            for num in nums:
                BREAK = False
                for base in temp_bases:
                    try:
                        temp = convert_base(int(num), base)
                    except ValueError:
                        continue
                    if self.puzzle_params.min_length <= len(temp) <= self.puzzle_params.max_length:
                        self.variables[i] = (temp, base)
                        self.hints[var.upper()] = "$"+r"\; ".join([
                            "(Base", f"{base})", f"{var}={sol_str.replace(num, var.upper(), 1)}",
                            "is", "a", "solution", "to", f"{sp.latex(expr)}={target}"]) + "$"
                        i += 1
                        temp_bases.remove(base)
                        BREAK = True
                        break
                if BREAK: break
        puzzles = [CrossWordPuzzle(num) for num, _ in self.variables]
        self.crossword_grid = create_crossword_grid(puzzles)
        self.puzzles = {p.num: p for p in puzzles}
        self.variables = {chr(65+i): self.variables[i] for i in range(self.puzzle_params.num_of_variables)}
        for var in self.hints:
            orientation = self.puzzles[self.variables[var][0]].orientation
            self.hints[var] = (self.hints[var], orientation)
        queue.put(self)

if __name__ == "__main__":
    q = multiprocessing.Queue()
    PuzzleManager(Difficulty.EASY, set(range(2, 11)), q)
    grid = q.get()
    print(grid.variables)
    print(grid.hints)
