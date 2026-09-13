from enum import Enum


class OptimizationType(str, Enum):
    """
    Type of the optimization problem: ``MINIMIZATION`` or ``MAXIMIZATION``.
    """

    MINIMIZATION = "minimization"
    MAXIMIZATION = "maximization"
