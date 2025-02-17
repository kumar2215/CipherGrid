import random
import sympy as sp

class MathProblem:

    LEVEL = None

    def __init__(self, max_topic_level: int=0): # NOQA
        self.initialise_subclasses()
        self.subclasses = [topic for topic in MathProblem.__subclasses__() if topic.LEVEL <= max_topic_level]

    @staticmethod
    def initialise_subclasses():
        import src.problem_generation.algebra
        import src.problem_generation.trigonometry
        import src.problem_generation.calculus
        # importing other math problem modules goes here

    def generate(self, complexity: int, var: sp.Symbol, target: sp.Integer, expr: sp.Expr = None, last_problem=None):
        if complexity <= 0: return expr, target
        subclasses = self.subclasses.copy()
        if last_problem and len(self.subclasses) > 1:
            subclasses = [s for s in self.subclasses if s != last_problem]
        problem = random.choice(subclasses)
        new_expr, other = problem().transform(var)
        expr = var if expr is None else expr
        try:
            new_target = problem.inverse(target, other)
        except Exception: # NOQA
            return self.generate(complexity, var, target, expr, last_problem)
        if (not new_target.is_real) or (not new_target.is_number) or not (-1e9 <= new_target <= 1e9):
            return self.generate(complexity, var, target, expr, problem)
        return self.generate(complexity - problem.LEVEL, var, new_target, expr.subs(var, new_expr), problem)

    def transform(self, a, b=None):
        raise NotImplementedError("Subclasses must implement this method")

    @staticmethod
    def inverse(expr, var):
        raise NotImplementedError("Subclasses must implement this method")
