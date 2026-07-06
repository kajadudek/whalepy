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
class AdaptiveWOAData(WOAData):
    a_strategy: str = "cosine"
    use_inertia_weight: bool = True
    adaptive_probability: bool = True
    p_start: float = 0.5
    p_end: float = 0.9

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.a_strategy not in {"cosine", "logarithmic"}:
            raise ValueError("a_strategy must be 'cosine' or 'logarithmic'.")
        if not 0.0 <= self.p_start <= 1.0:
            raise ValueError("p_start must be between 0.0 and 1.0.")
        if not 0.0 <= self.p_end <= 1.0:
            raise ValueError("p_end must be between 0.0 and 1.0.")


@dataclass
class CWOAData(WOAData):
    chaotic_map: str = "logistic"
    chaotic_seed: Optional[float] = 0.37
    use_chaotic_initialization: bool = True
    use_chaotic_probability: bool = True
    use_chaotic_coefficients: bool = True
    use_chaotic_spiral: bool = True
    use_chaotic_a: bool = False
    logistic_a: float = 4.0
    sine_a: float = 4.0

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.chaotic_map not in {"logistic", "tent", "sine"}:
            raise ValueError("chaotic_map must be 'logistic', 'tent', or 'sine'.")
        if self.chaotic_seed is None:
            self.chaotic_seed = 0.37
        if not 0.0 < self.chaotic_seed < 1.0:
            raise ValueError("chaotic_seed must be between 0.0 and 1.0.")


@dataclass
class ModifiedSpiralWOAData(WOAData):
    spiral_mode: str = "archimedean"
    spiral_b: float = 1.0
    spiral_step: float = 0.25
    spiral_shrink_factor: float = 0.75

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.spiral_mode not in {"logarithmic", "archimedean"}:
            raise ValueError("spiral_mode must be 'logarithmic' or 'archimedean'.")
        if self.spiral_step < 0.0:
            raise ValueError("spiral_step must be non-negative.")
        if self.spiral_shrink_factor < 0.0:
            raise ValueError("spiral_shrink_factor must be non-negative.")


@dataclass
class MutationWOAData(WOAData):
    mutation_strategy: str = "de_rand_1"
    mutation_factor: float = 0.5
    mutation_probability: float = 0.3
    use_mutation_selection: bool = True

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.mutation_strategy != "de_rand_1":
            raise ValueError("mutation_strategy must be 'de_rand_1'.")
        if self.mutation_factor <= 0.0:
            raise ValueError("mutation_factor must be greater than 0.0.")
        if not 0.0 <= self.mutation_probability <= 1.0:
            raise ValueError("mutation_probability must be between 0.0 and 1.0.")


@dataclass
class LevyWalkWOAData(BaseData):
    levy_beta: float = 1.5
    random_walk_rate: float = 0.1
    walk_strategy_name: str = "placeholder"
