from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Optional

from whalepy.models.enums.boundary_constrain import BoundaryConstraint
from whalepy.models.enums.optimization import OptimizationType


@dataclass
class BaseData:
    population_size: int = 30
    max_iter: Optional[int] = 100
    max_nfe: Optional[int] = None
    dimension: int = 10
    lb: list[float] = field(default_factory=list)
    ub: list[float] = field(default_factory=list)
    optimization_type: OptimizationType = OptimizationType.MINIMIZATION
    function: Optional[Callable[..., Any]] = None
    boundary_constraints_fun: BoundaryConstraint | str | Callable[..., Any] = BoundaryConstraint.CLIP
    log_population: bool = False
    parallel_processing: bool = False
    show_plots: bool = False
    stop_condition: Any = None
    seed: Optional[int] = None
    notes: str = ""

    def __post_init__(self) -> None:
        if self.population_size <= 0:
            raise ValueError("population_size must be greater than 0.")
        if self.dimension <= 0:
            raise ValueError("dimension must be greater than 0.")
        if self.max_iter is None and self.max_nfe is None:
            self.max_iter = 100
        if self.max_iter is not None and self.max_iter <= 0:
            raise ValueError("max_iter must be greater than 0 when provided.")
        if self.max_nfe is not None and self.max_nfe <= 0:
            raise ValueError("max_nfe must be greater than 0 when provided.")

        self.lb = self._normalize_bounds(self.lb, "lb")
        self.ub = self._normalize_bounds(self.ub, "ub")

        for lower_bound, upper_bound in zip(self.lb, self.ub):
            if lower_bound >= upper_bound:
                raise ValueError("Each lower bound must be smaller than its upper bound.")

    def _normalize_bounds(self, bounds: list[float], field_name: str) -> list[float]:
        if not bounds:
            raise ValueError(f"{field_name} must be provided.")
        if len(bounds) == 1 and self.dimension > 1:
            return [float(bounds[0])] * self.dimension
        if len(bounds) != self.dimension:
            raise ValueError(f"{field_name} must have length equal to dimension.")
        return [float(value) for value in bounds]


@dataclass
class WOAData(BaseData):
    shrink_coefficient_strategy: str = "linear"
    encircling_probability: float = 0.5
    spiral_constant: float = 1.0


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
