from __future__ import annotations

import math
import random
from abc import ABC, abstractmethod
from typing import Optional

from whalepy.WOAAlgs.data.alg_data import BaseData
from whalepy.models.algorithm_result import AlgorithmResult
from whalepy.models.enums.optimization import OptimizationType
from whalepy.models.fitness_function import FitnessFunction, coerce_fitness_function
from whalepy.models.population import Population
from whalepy.models.stop_condition.never_stop_condition import NeverStopCondition
from whalepy.models.stop_condition.stop_condition import StopCondition
from whalepy.models.whale import Whale


class BaseWOAAlg(ABC):
    """
    Base class of all WOA variants.

    It implements the common optimization loop: initialization and evaluation of the
    population, tracking of the best solution found so far (``best_whale``, which is the
    leader ``X*`` used in the position updates) and of the worst whale in the current
    population (``worst_whale``), checking of the stopping criteria, and preparation of the
    result. Each variant implements :meth:`next_epoch`, which performs a single iteration.

    Parameters:
        config: Configuration of the variant (an instance of a subclass of
            :class:`~whalepy.BaseData`).
        stop_condition: Optional stopping condition. If not given, ``config.stop_condition``
            is used.
    """

    def __init__(
            self,
            config: BaseData,
            stop_condition: Optional[StopCondition] = None,
    ) -> None:
        self.config = config
        self.stop_condition = stop_condition or config.stop_condition or NeverStopCondition()
        self.fitness_function: FitnessFunction = coerce_fitness_function(config.function)
        self.population = Population()
        self.best_whale: Optional[Whale] = None
        self.worst_whale: Optional[Whale] = None
        self.history: list[float] = []
        self.current_epoch = 0
        self.rng = random.Random(config.seed)
        self.initialized = False
        self.max_iter_reference = self._resolve_max_iter_reference()

    def _initialize(self) -> None:
        if self.config.max_nfe is not None and self.config.max_nfe < self.config.population_size:
            raise ValueError("max_nfe must be at least population_size for the initial evaluation.")

        self.population.initialize_whales(
            population_size=self.config.population_size,
            dimension=self.config.dimension,
            lb=self.config.lb,
            ub=self.config.ub,
            rng=self.rng,
        )
        self.population.update_fitness_values(self.fitness_function)
        self._refresh_population_state()
        if self.best_whale is not None and self.best_whale.fitness_value is not None:
            self.history = [self.best_whale.fitness_value]
        self.initialized = True

    def run(self) -> AlgorithmResult:
        """
        Runs the optimization until ``max_iter`` or ``max_nfe`` is reached or the stopping
        condition is met.

        Returns:
            AlgorithmResult: The best solution found, statistics of the final population, and
            the convergence history.
        """
        if not self.initialized:
            self._initialize()

        if self.stop_condition.should_stop(self, self.best_whale):
            return self._build_result()

        while self._can_continue():
            self.next_epoch()
            self.current_epoch += 1
            self.population.epoch = self.current_epoch
            if self.best_whale is not None and self.best_whale.fitness_value is not None:
                self.history.append(self.best_whale.fitness_value)
            if self.stop_condition.should_stop(self, self.best_whale):
                break

        return self._build_result()

    def _refresh_population_state(self) -> None:
        # best_whale is the best solution found so far (the leader X* and the
        # returned result); worst_whale refers to the current population.
        current_best = self.population.get_best_whale(self.config.optimization_type)
        if current_best is not None and current_best.fitness_value is not None and (
                self.best_whale is None
                or self.best_whale.fitness_value is None
                or self._is_better(current_best.fitness_value, self.best_whale.fitness_value)
        ):
            self.best_whale = current_best
        self.worst_whale = self.population.get_worst_whale(self.config.optimization_type)

    def _is_better(self, candidate: float, reference: float) -> bool:
        if self.config.optimization_type == OptimizationType.MAXIMIZATION:
            return candidate > reference
        return candidate < reference

    def initialization_nfe_cost(self) -> int:
        """
        Number of objective function evaluations used by the initialization.
        """
        return int(self.config.population_size)

    def epoch_nfe_cost(self) -> int:
        """
        Number of objective function evaluations used by a single iteration.
        """
        return int(self.config.population_size)

    def _resolve_max_iter_reference(self) -> int:
        if self.config.max_iter is not None:
            return max(1, self.config.max_iter)
        if self.config.max_nfe is not None:
            init_cost = int(self.initialization_nfe_cost())
            per_iter_cost = int(self.epoch_nfe_cost())
            if per_iter_cost <= 0:
                return 1
            remaining_evaluations = max(int(self.config.max_nfe) - init_cost, 0)
            estimated_iterations = math.ceil(remaining_evaluations / per_iter_cost)
            return max(1, int(estimated_iterations))
        return 1

    def _can_continue(self) -> bool:
        if self.config.max_iter is not None and self.current_epoch >= self.config.max_iter:
            return False
        if self.config.max_nfe is not None and self.fitness_function.evaluations >= self.config.max_nfe:
            return False
        return True

    def _build_result(self) -> AlgorithmResult:
        return AlgorithmResult(
            best_whale=self.best_whale.copy() if self.best_whale is not None else None,
            worst_whale=self.worst_whale.copy() if self.worst_whale is not None else None,
            best_fitness_value=None if self.best_whale is None else self.best_whale.fitness_value,
            worst_fitness_value=None if self.worst_whale is None else self.worst_whale.fitness_value,
            mean_fitness_value=self.population.mean_fitness(),
            std_fitness_value=self.population.std_fitness(),
            history=list(self.history),
            success=self.best_whale is not None,
            message=f"{self.__class__.__name__} finished.",
            epochs_completed=self.current_epoch,
            nfe=self.fitness_function.evaluations,
        )

    @abstractmethod
    def next_epoch(self) -> None:
        """
        Performs a single iteration of the algorithm. Implemented by each variant.
        """
        raise NotImplementedError


BaseWOA = BaseWOAAlg
