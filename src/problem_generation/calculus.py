import random
from src.problem_generation.generate import MathProblem
import sympy as sp

class IntegrationProblem(MathProblem):

    LEVEL = 5

    def __init__(self):
        super().__init__()
        self.range = tuple(map(int, (-1e3, 1e3)))

    def transform(self, a, b=None):
        gen = MathProblem(2)
        if b is None: b = random.randint(*self.range)
        expr, target = gen.generate(2, sp.Symbol("x"), sp.Integer(b), None,
                            IntegrationProblem)
        return sp.integrate(expr, (sp.Symbol("x"), 0, a)), a

    @staticmethod
    def inverse(expr, var):
        return sp.diff(expr, var)
