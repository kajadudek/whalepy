from enum import Enum


class OptimizationType(str, Enum):
    MINIMIZATION = "minimization"
    MAXIMIZATION = "maximization"
