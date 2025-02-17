import random
from src.problem_generation.generate import MathProblem
import sympy as sp

class AdditionProblem(MathProblem):

    LEVEL = 1

    def __init__(self):
        super().__init__()
        self.range = tuple(map(int, (-1e3, 1e3)))

    def transform(self, a, b=None):
        while b in (0, None): b = random.randint(*self.range)
        return a + b, b
    
    @staticmethod
    def inverse(expr, var):
        return expr - var

class SubtractionProblem(MathProblem):

    LEVEL = 1

    def __init__(self):
        super().__init__()
        self.range = tuple(map(int, (-1e3, 1e3)))

    def transform(self, a, b=None):
        while b in (0, None): b = random.randint(*self.range)
        return a - b, b
    
    @staticmethod
    def inverse(expr, var):
        return expr + var

class MultiplicationProblem(MathProblem):

    LEVEL = 2

    def __init__(self):
        super().__init__()
        self.range = tuple(map(int, (-1e2, 1e2)))

    def transform(self, a, b=None):
        while b in (0, None): b = random.randint(*self.range)
        return a * b, b
    
    @staticmethod
    def inverse(expr, var):
        return expr / var

class DivisionProblem(MathProblem):

    LEVEL = 2

    def __init__(self):
        super().__init__()
        self.range = tuple(map(int, (-1e2, 1e2)))

    def transform(self, a, b=None):
        while b in (0, None): b = random.randint(*self.range)
        return a / b, b
    
    @staticmethod
    def inverse(expr, var):
        return expr * var

class ExponentiationProblem(MathProblem):

    LEVEL = 3

    def __init__(self):
        super().__init__()
        self.range = tuple(map(int, (-3, 3)))

    def transform(self, a, b=None):
        while b in (0, None): b = random.randint(*self.range)
        return a ** b, b
    
    @staticmethod
    def inverse(expr, var):
        return expr ** (1 / var)

class LogarithmProblem(MathProblem):

    LEVEL = 3

    def __init__(self,):
        super().__init__()
        self.range = tuple(map(int, (2, 5)))

    def transform(self, a, b=None):
        if b is None: b = random.randint(*self.range)
        return sp.log(a, b), b

    @staticmethod
    def inverse(expr, var):
        return var ** expr
