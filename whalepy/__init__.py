from whalepy.WOAAlgs import (
    AdaptiveWOA,
    CWOA,
    ExponentialDecayWOA,
    GaussianWOA,
    LevyWalkWOA,
    ModifiedSpiralWOA,
    MutationWOA,
    OppositionBasedWOA,
    SingleDimensionalWOA,
    WOA,
    WorstIndividualDisturbanceWOA,
)
from whalepy.WOAAlgs.data import (
    AdaptiveWOAData,
    BaseData,
    CWOAData,
    ExponentialDecayWOAData,
    GaussianWOAData,
    LevyWalkWOAData,
    ModifiedSpiralWOAData,
    MutationWOAData,
    OppositionWOAData,
    SingleDimensionalWOAData,
    WOAData,
    WorstIndividualDisturbanceWOAData,
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
    "ExponentialDecayWOA",
    "ExponentialDecayWOAData",
    "FunctionLoader",
    "GaussianWOA",
    "GaussianWOAData",
    "LevyWalkWOA",
    "LevyWalkWOAData",
    "ModifiedSpiralWOA",
    "ModifiedSpiralWOAData",
    "MutationWOA",
    "MutationWOAData",
    "OppositionBasedWOA",
    "OppositionWOAData",
    "OptimizationType",
    "SingleDimensionalWOA",
    "SingleDimensionalWOAData",
    "Whale",
    "WOA",
    "WOAData",
    "WorstIndividualDisturbanceWOA",
    "WorstIndividualDisturbanceWOAData",
    "run_algorithm",
]
