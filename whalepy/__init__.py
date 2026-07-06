from whalepy.WOAAlgs import (
    AdaptiveWOA,
    CWOA,
    LevyWalkWOA,
    ModifiedSpiralWOA,
    MutationWOA,
    WOA,
)
from whalepy.WOAAlgs.data import (
    AdaptiveWOAData,
    BaseData,
    CWOAData,
    LevyWalkWOAData,
    ModifiedSpiralWOAData,
    MutationWOAData,
    WOAData,
)
from whalepy.functions import FunctionLoader
from whalepy.models.algorithm_result import AlgorithmResult
from whalepy.models.enums.boundary_constrain import BoundaryConstraint
from whalepy.models.enums.optimization import OptimizationType
from whalepy.models.whale import Whale


def run_algorithm(algorithm_cls, config):
    return algorithm_cls(config).run()


__all__ = [
    "AdaptiveWOA",
    "AdaptiveWOAData",
    "AlgorithmResult",
    "BaseData",
    "BoundaryConstraint",
    "CWOA",
    "CWOAData",
    "FunctionLoader",
    "LevyWalkWOA",
    "LevyWalkWOAData",
    "ModifiedSpiralWOA",
    "ModifiedSpiralWOAData",
    "MutationWOA",
    "MutationWOAData",
    "OptimizationType",
    "Whale",
    "WOA",
    "WOAData",
    "run_algorithm",
]
