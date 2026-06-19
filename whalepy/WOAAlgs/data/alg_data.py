from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Optional

from whalepy.models.enums.optimization import OptimizationType


@dataclass
class BaseData:
    population_size: int = 30
    max_nfe: int = 1000
    dimension: int = 10
    lb: list[float] = field(default_factory=list)
    ub: list[float] = field(default_factory=list)
    optimization_type: OptimizationType = OptimizationType.MINIMIZATION
    function: Optional[Callable[..., Any]] = None
    log_population: bool = False
    parallel_processing: bool = False
    show_plots: bool = False
    seed: Optional[int] = None
    notes: str = ""


@dataclass
class WOAData(BaseData):
    shrink_coefficient_strategy: str = "linear"
    encircling_probability: float = 0.5


@dataclass
class AdaptiveWOAData(BaseData):
    adaptation_window: int = 10
    adaptation_rule: str = "todo"
    adaptive_schedule_name: str = "placeholder"


@dataclass
class CWOAData(BaseData):
    chaotic_map_name: str = "placeholder"
    chaotic_seed: Optional[float] = None
    reinitialization_interval: int = 0


@dataclass
class ModifiedSpiralWOAData(BaseData):
    spiral_mode: str = "placeholder"
    spiral_shape_factor: float = 1.0
    spiral_schedule_name: str = "todo"


@dataclass
class MutationWOAData(BaseData):
    mutation_rate: float = 0.1
    mutation_operator_name: str = "placeholder"
    elitism_enabled: bool = False


@dataclass
class LevyWalkWOAData(BaseData):
    levy_beta: float = 1.5
    random_walk_rate: float = 0.1
    walk_strategy_name: str = "placeholder"
