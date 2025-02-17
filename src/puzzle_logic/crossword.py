import random
from enum import Enum

class Orientation(Enum):
    LEFT_TO_RIGHT = 0
    TOP_TO_BOTTOM = 1

def convert_base(num: int, base: int) -> str:
    if num == 0: return "0"
    digits = []
    while num:
        digits.append(str(num % base))
        num //= base
    return "".join(digits[::-1])

def generate_random_numbers(N: int, min_length: int, max_length: int) -> list[tuple[str, int]]:
    result = []
    i = 0
    while i < N:
        num = random.randint(10**(min_length-1), 10**max_length - 1)
        base = random.choice(list(range(2, 11)))
        temp = convert_base(num, base)
        if min_length <= len(temp) <= max_length:
            result.append((temp, base))
            i += 1
    return result

class CrossWordPuzzle:

    def __init__(self, num: str):
        self.num = num
        self.orientation = None
        self.start = None

    def get_intersections(self, other: "CrossWordPuzzle") -> dict[tuple[int, int], str]:
        if self.orientation == other.orientation: return {}
        intersections = {}
        for i, digit1 in enumerate(self.num):
            for j, digit2 in enumerate(other.num):
                if digit1 == digit2 and 0 < i < len(self.num)-1 and 0 <= j < len(other.num)-1:
                    intersections[(i, j)] = digit1
        # print(f"Intersections between {self.num} and {other.num}: {intersections}")
        keys = list(intersections.keys())
        random.shuffle(keys)
        return {k: intersections[k] for k in keys}

class CrossWordGrid:

    def __init__(self):
        self.points = {}
        self.puzzles = []
        self.intersections = set()
        self.height = 0
        self.width = 0
        self.next_orientation = Orientation.LEFT_TO_RIGHT

    def adjust(self):
        L, R, T, B = 0, 0, 0, 0
        for pos in self.points:
            L = min(L, pos[0])
            R = max(R, pos[0])
            T = min(T, pos[1])
            B = max(B, pos[1])
        new_points = {}
        new_intersections = set()
        for point in self.points:
            new_points[(point[0] - L, point[1] - T)] = self.points[point]
        for intersection in self.intersections:
            new_intersections.add((intersection[0] - L, intersection[1] - T))
        for puzzle in self.puzzles:
            puzzle.start = (puzzle.start[0] - L, puzzle.start[1] - T)
        self.points = new_points
        self.width = R - L + 1
        self.height = B - T + 1
        return self.width * self.height

    def can_add(self, puzzle: CrossWordPuzzle, start: tuple[int, int], intersection: tuple[int, int]) -> bool:
        if self.next_orientation == Orientation.LEFT_TO_RIGHT:
            for i in range(len(puzzle.num)):
                if self.points.get((start[0] + i, start[1]), puzzle.num[i]) != puzzle.num[i]:
                    return False
                pt = (start[0] + i, start[1])
                if pt != intersection:
                    top = (pt[0], pt[1] - 1)
                    bottom = (pt[0], pt[1] + 1)
                    if top in self.points or bottom in self.points: return False
                    if pt == start:
                        left = (pt[0] - 1, pt[1])
                        if left in self.points or left in self.intersections: return False
                    if pt == (start[0] + len(puzzle.num) - 1, start[1]):
                        right = (pt[0] + 1, pt[1])
                        if right in self.points or right in self.intersections: return False
        else:
            for i in range(len(puzzle.num)):
                if self.points.get((start[0], start[1] + i), puzzle.num[i]) != puzzle.num[i]:
                    return False
                pt = (start[0], start[1] + i)
                if pt != intersection:
                    left = (pt[0] - 1, pt[1])
                    right = (pt[0] + 1, pt[1])
                    if left in self.points or right in self.points:
                        return False
                    if pt == start:
                        top = (pt[0], pt[1] - 1)
                        if top in self.points or top in self.intersections: return False
                    if pt == (start[0], start[1] + len(puzzle.num) - 1):
                        bottom = (pt[0], pt[1] + 1)
                        if bottom in self.points or bottom in self.intersections: return False
        return True

    def add(self, puzzle: CrossWordPuzzle, start: tuple[int, int], intersection: tuple[int, int]):
        self.points[start] = puzzle.num[0]
        if self.next_orientation == Orientation.LEFT_TO_RIGHT:
            for i in range(1, len(puzzle.num)):
                self.points[(start[0] + i, start[1])] = puzzle.num[i]
        else:
            for i in range(1, len(puzzle.num)):
                self.points[(start[0], start[1] + i)] = puzzle.num[i]
        puzzle.orientation = self.next_orientation
        puzzle.start = start
        self.puzzles.append(puzzle)
        self.intersections.add(intersection)
        self.adjust()
        if self.next_orientation == Orientation.LEFT_TO_RIGHT:
            self.next_orientation = Orientation.TOP_TO_BOTTOM
        else:
            self.next_orientation = Orientation.LEFT_TO_RIGHT

    def add_puzzle(self, new_puzzle: CrossWordPuzzle):
        if not self.puzzles:
            self.add(new_puzzle, (0, 0), (0, 0))
            return True
        else:
            new_puzzle.orientation = self.next_orientation
            STOP = False
            for puzzle in self.puzzles:
                if puzzle.orientation == new_puzzle.orientation: continue
                intersections = puzzle.get_intersections(new_puzzle)
                for intersection, digit in intersections.items():
                    if puzzle.orientation == Orientation.LEFT_TO_RIGHT:
                        start = (puzzle.start[0] + intersection[0], puzzle.start[1] - intersection[1])
                        actual_intersection = (start[0], puzzle.start[1])
                    else:
                        start = (puzzle.start[0] - intersection[1], puzzle.start[1] + intersection[0])
                        actual_intersection = (puzzle.start[0], start[1])
                    if self.can_add(new_puzzle, start, actual_intersection):
                        self.add(new_puzzle, start, actual_intersection)
                        STOP = True
                        break
                if STOP: break
            return STOP

    def print_grid(self):
        for i in range(self.height):
            for j in range(self.width):
                print(self.points.get((j, i), "."), end=" ")
            print()

def create_crossword_grid(puzzles: list[CrossWordPuzzle]) -> CrossWordGrid:
    while True:
        random.shuffle(puzzles)
        successful = [False] * len(puzzles)
        crossword_grid = CrossWordGrid()
        for i, puzzle in enumerate(puzzles):
            successful[i] = crossword_grid.add_puzzle(puzzle)
        if all(successful):
            grid = [["."] * crossword_grid.width for _ in range(crossword_grid.height)]
            for i in range(crossword_grid.height):
                for j in range(crossword_grid.width):
                    grid[i][j] = crossword_grid.points.get((j, i), ".")
            crossword_grid.grid = grid
            return crossword_grid

if __name__ == "__main__":
    random_numbers = generate_random_numbers(8, 4, 7)
    print(f"Random numbers: {random_numbers}")
    CROSSWORD_PUZZLES = [CrossWordPuzzle(num) for num, _ in random_numbers]
    CROSSWORD_GRID = create_crossword_grid(CROSSWORD_PUZZLES)
