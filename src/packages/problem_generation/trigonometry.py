from packages.problem_generation.generate import MathProblem
import sympy as sp

class SinProblem(MathProblem):

    LEVEL = 4

    def __init__(self):
        super().__init__()

    def transform(self, a, b=None):
        return sp.sin(a), b

    @staticmethod
    def inverse(expr, var):
        return sp.asin(expr)

class CosProblem(MathProblem):

    LEVEL = 4

    def __init__(self):
        super().__init__()

    def transform(self, a, b=None):
        return sp.cos(a), b

    @staticmethod
    def inverse(expr, var):
        return sp.acos(expr)

class TanProblem(MathProblem):

    LEVEL = 4

    def __init__(self):
        super().__init__()

    def transform(self, a, b=None):
        return sp.tan(a), b

    @staticmethod
    def inverse(expr, var):
        return sp.atan(expr)

class CscProblem(MathProblem):

    LEVEL = 4

    def __init__(self):
        super().__init__()

    def transform(self, a, b=None):
        return 1/sp.sin(a), b

    @staticmethod
    def inverse(expr, var):
        return sp.asin(1/expr)

class SecProblem(MathProblem):

    LEVEL = 4

    def __init__(self):
        super().__init__()

    def transform(self, a, b=None):
        return 1/sp.cos(a), b

    @staticmethod
    def inverse(expr, var):
        return sp.acos(1/expr)

class CotProblem(MathProblem):

    LEVEL = 4

    def __init__(self):
        super().__init__()

    def transform(self, a, b=None):
        return 1/sp.tan(a), b

    @staticmethod
    def inverse(expr, var):
        return sp.atan(1/expr)

class ArcSinProblem(MathProblem):

    LEVEL = 4

    def __init__(self):
        super().__init__()

    def transform(self, a, b=None):
        return sp.asin(a), b

    @staticmethod
    def inverse(expr, var):
        return sp.sin(expr)

class ArcCosProblem(MathProblem):

    LEVEL = 4

    def __init__(self):
        super().__init__()

    def transform(self, a, b=None):
        return sp.acos(a), b

    @staticmethod
    def inverse(expr, var):
        return sp.cos(expr)

class ArcTanProblem(MathProblem):

    LEVEL = 4

    def __init__(self):
        super().__init__()

    def transform(self, a, b=None):
        return sp.atan(a), b

    @staticmethod
    def inverse(expr, var):
        return sp.tan(expr)

class ArcCscProblem(MathProblem):

    LEVEL = 4

    def __init__(self):
        super().__init__()

    def transform(self, a, b=None):
        return sp.asin(1/a), b

    @staticmethod
    def inverse(expr, var):
        return 1/sp.sin(expr)

class ArcSecProblem(MathProblem):

    LEVEL = 4

    def __init__(self):
        super().__init__()

    def transform(self, a, b=None):
        return sp.acos(1/a), b

    @staticmethod
    def inverse(expr, var):
        return 1/sp.cos(expr)

class ArcCotProblem(MathProblem):

    LEVEL = 4

    def __init__(self):
        super().__init__()

    def transform(self, a, b=None):
        return sp.atan(1/a), b

    @staticmethod
    def inverse(expr, var):
        return 1/sp.tan(expr)
