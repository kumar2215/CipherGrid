from enum import Enum

class Difficulty(Enum):
    EASY = 1
    MEDIUM = 2
    HARD = 3

DIFFICULTY_TO_COLOR = {
    Difficulty.EASY: "green",
    Difficulty.MEDIUM: "orange",
    Difficulty.HARD: "red"
}
