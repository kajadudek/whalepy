from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Optional

from whalepy.models.enums.boundary_constrain import BoundaryConstraint
from whalepy.models.enums.optimization import OptimizationType


@dataclass
class BaseData:
    """
    Parameters shared by all WOA variants.

    Parameters:
        population_size: Number of whales in the population. Default: 30.
        max_iter: Maximum number of iterations. Default: 100. If both ``max_iter`` and
            ``max_nfe`` are None, 100 iterations are used.
        max_nfe: Maximum number of objective function evaluations. Default: None (no limit).
            If both limits are given, the run stops when the first of them is reached.
        dimension: Number of decision variables. Default: 10.
        lb: Lower bounds of the decision variables. If a single value is given, it is used
            for all dimensions. Required.
        ub: Upper bounds of the decision variables. If a single value is given, it is used
            for all dimensions. Required.
        optimization_type: ``OptimizationType.MINIMIZATION`` (default) or
            ``OptimizationType.MAXIMIZATION``.
        function: Objective function. Any Python function that takes a list of decision
            variables and returns a number, or a benchmark function loaded with
            :class:`~whalepy.FunctionLoader`. Required.
        boundary_constraints_fun: Method used when a whale leaves the search space:
            ``BoundaryConstraint.CLIP`` (default), ``BoundaryConstraint.REFLECT``,
            ``BoundaryConstraint.RANDOM_RESET``, ``BoundaryConstraint.NONE``, or a user-defined
            function ``f(candidate, lb, ub)`` that returns the repaired position.
        stop_condition: Optional user-defined stopping condition
            (:class:`~whalepy.models.stop_condition.StopCondition`), checked after the
            initialization and after each iteration. Default: None.
        seed: Seed of the random number generator, which makes the results reproducible.
            Default: None.
    """

    population_size: int = 30
    max_iter: Optional[int] = 100
    max_nfe: Optional[int] = None
    dimension: int = 10
    lb: list[float] = field(default_factory=list)
    ub: list[float] = field(default_factory=list)
    optimization_type: OptimizationType = OptimizationType.MINIMIZATION
    function: Optional[Callable[..., Any]] = None
    boundary_constraints_fun: BoundaryConstraint | str | Callable[..., Any] = BoundaryConstraint.CLIP
    stop_condition: Any = None
    seed: Optional[int] = None

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
    """
    Configuration of the original WOA (:class:`~whalepy.WOA`) and the base configuration of
    all variants. Inherits the parameters of :class:`~whalepy.BaseData`.

    Parameters:
        encircling_probability: Probability of the encircling or exploration move instead of
            the spiral move. Used only by :class:`~whalepy.AdaptiveWOA` when
            ``adaptive_probability`` is False; the other variants use the value 0.5 of the
            original algorithm. Default: 0.5.
        spiral_constant: Constant ``b`` defining the shape of the logarithmic spiral.
            Default: 1.0.
    """

    encircling_probability: float = 0.5
    spiral_constant: float = 1.0


@dataclass
class AdaptiveWOAData(WOAData):
    """
    Configuration of :class:`~whalepy.AdaptiveWOA`. Inherits the parameters of
    :class:`~whalepy.WOAData`.

    Parameters:
        a_strategy: Nonlinear schedule of the coefficient ``a``: ``"cosine"``
            (``a = 2 cos(pi t / (2T))``) or ``"logarithmic"`` (``a = 2 - log10(1 + 9 t / T)``).
            Default: ``"cosine"``.
        use_inertia_weight: If True, the position of the leader in the encircling move is
            multiplied by an inertia weight that increases linearly from 0.5 to 1.0.
            Default: True.
        adaptive_probability: If True, the probability of the spiral move increases linearly
            from ``p_start`` to ``p_end`` during the run; otherwise it is equal to
            ``1 - encircling_probability``. Default: True.
        p_start: Probability of the spiral move at the beginning of the run. Default: 0.5.
        p_end: Probability of the spiral move at the end of the run. Default: 0.9.
    """

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
    """
    Configuration of :class:`~whalepy.CWOA`. Inherits the parameters of
    :class:`~whalepy.WOAData`.

    Parameters:
        chaotic_map: Chaotic map used to generate the chaotic values: ``"logistic"``,
            ``"tent"`` or ``"sine"``. Default: ``"logistic"``.
        chaotic_seed: Initial value of the chaotic map, from the interval (0, 1). If None,
            it is derived from ``seed``. Default: None.
        use_chaotic_initialization: If True, the initial positions are generated with the
            chaotic map. Default: True.
        use_chaotic_probability: If True, the random number ``p`` that selects the move is
            replaced with a chaotic value. Default: True.
        use_chaotic_coefficients: If True, the random numbers ``r1`` and ``r2`` used in the
            coefficients ``A`` and ``C`` are replaced with chaotic values. Default: True.
        use_chaotic_spiral: If True, the spiral parameter ``l`` is generated with the chaotic
            map. Default: True.
        use_chaotic_a: If True, the coefficient ``a`` is additionally multiplied by a chaotic
            value. Default: False.
        logistic_a: Control parameter of the logistic map. Default: 4.0.
        sine_a: Control parameter of the sine map. Default: 4.0.
    """

    chaotic_map: str = "logistic"
    chaotic_seed: Optional[float] = None
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
        if self.chaotic_seed is not None and not 0.0 < self.chaotic_seed < 1.0:
            raise ValueError("chaotic_seed must be between 0.0 and 1.0.")


@dataclass
class ModifiedSpiralWOAData(WOAData):
    """
    Configuration of :class:`~whalepy.ModifiedSpiralWOA`. Inherits the parameters of
    :class:`~whalepy.WOAData`.

    Parameters:
        spiral_mode: Shape of the spiral used in the bubble-net attack: ``"archimedean"`` or
            ``"logarithmic"`` (the spiral of the original WOA). Default: ``"archimedean"``.
        spiral_b: Constant ``b`` of the logarithmic spiral (used when ``spiral_mode`` is
            ``"logarithmic"``). Default: 1.0.
        spiral_step: Growth rate of the radius of the Archimedean spiral with ``|l|``.
            Default: 0.25.
        spiral_shrink_factor: Additional radius of the Archimedean spiral, which decreases
            linearly to zero during the run. Default: 0.75.
    """

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
    """
    Configuration of :class:`~whalepy.MutationWOA`. Inherits the parameters of
    :class:`~whalepy.WOAData`. The population must contain at least 4 whales.

    Parameters:
        mutation_strategy: Mutation strategy. Currently only ``"de_rand_1"`` (DE/rand/1) is
            available. Default: ``"de_rand_1"``.
        mutation_factor: Scale factor ``F`` of the DE/rand/1 mutation. Default: 0.5.
        mutation_probability: Probability that a mutation candidate is created for a whale;
            it is also the probability of taking each coordinate of this candidate from the
            mutant vector instead of the WOA candidate. Default: 0.3.
        use_mutation_selection: If True, the better of the WOA candidate and the mutation
            candidate is kept; otherwise the mutation candidate always replaces the WOA
            candidate. Default: True.
    """

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
class LevyWalkWOAData(WOAData):
    """
    Configuration of :class:`~whalepy.LevyWalkWOA`. Inherits the parameters of
    :class:`~whalepy.WOAData`.

    Parameters:
        levy_beta: Stability index ``beta`` of the Levy distribution (Mantegna's algorithm),
            from the interval (0, 2]. Default: 1.5.
        levy_scale: Scale of the Levy flight step. Default: 0.05.
        use_levy_exploration: If True, the exploration move is replaced with a Levy flight.
            Default: True.
        levy_mode: ``"exploration_only"`` uses the Levy flight candidate, ``"hybrid"`` uses
            the average of the Levy flight candidate and the standard exploration move.
            Default: ``"exploration_only"``.
    """

    levy_beta: float = 1.5
    levy_scale: float = 0.05
    use_levy_exploration: bool = True
    levy_mode: str = "exploration_only"

    def __post_init__(self) -> None:
        super().__post_init__()
        if not 0.0 < self.levy_beta <= 2.0:
            raise ValueError("levy_beta must be in the interval (0.0, 2.0].")
        if self.levy_scale <= 0.0:
            raise ValueError("levy_scale must be greater than 0.0.")
        if self.levy_mode not in {"exploration_only", "hybrid"}:
            raise ValueError("levy_mode must be 'exploration_only' or 'hybrid'.")


@dataclass
class GaussianWOAData(WOAData):
    """
    Configuration of :class:`~whalepy.GaussianWOA`. Uses the parameters of
    :class:`~whalepy.WOAData`; the variant has no additional parameters.
    """


@dataclass
class OppositionWOAData(WOAData):
    """
    Configuration of :class:`~whalepy.OppositionBasedWOA`. Inherits the parameters of
    :class:`~whalepy.WOAData`.

    Parameters:
        use_obl_initialization: If True, the initial population is selected from the random
            population and its opposite population (2 * ``population_size`` evaluations).
            Default: True.
    """

    use_obl_initialization: bool = True


@dataclass
class SingleDimensionalWOAData(WOAData):
    """
    Configuration of :class:`~whalepy.SingleDimensionalWOA`. Uses the parameters of
    :class:`~whalepy.WOAData`; the variant has no additional parameters.
    """


@dataclass
class WorstIndividualDisturbanceWOAData(WOAData):
    """
    Configuration of :class:`~whalepy.WorstIndividualDisturbanceWOA`. Uses the parameters of
    :class:`~whalepy.WOAData`; the variant has no additional parameters.
    """


@dataclass
class ExponentialDecayWOAData(WOAData):
    """
    Configuration of :class:`~whalepy.ExponentialDecayWOA`. Inherits the parameters of
    :class:`~whalepy.WOAData`. The coefficient ``a`` follows the schedule
    ``a(t) = a_initial - (a_initial - a_final) * (exp(tau ** k) - 1) / (e - 1)``,
    where ``tau = t / (T - 1)``.

    Parameters:
        a_initial: Value of ``a`` in the first iteration. Default: 2.0.
        a_final: Value of ``a`` in the last iteration. Default: 0.0.
        k: Shape parameter of the schedule (``k > 0``). Default: 0.5.
    """

    a_initial: float = 2.0
    a_final: float = 0.0
    k: float = 0.5

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.a_initial <= 0.0:
            raise ValueError("a_initial must be greater than 0.0.")
        if self.a_final < 0.0:
            raise ValueError("a_final must be greater than or equal to 0.0.")
        if self.a_final >= self.a_initial:
            raise ValueError("a_final must be strictly smaller than a_initial.")
        if self.k <= 0.0:
            raise ValueError("k must be greater than 0.0.")
