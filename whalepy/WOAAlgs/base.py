from __future__ import annotations

import math
import random
from abc import ABC, abstractmethod
from typing import Optional

from whalepy.WOAAlgs.data.alg_data import BaseData
from whalepy.models.algorithm_result import AlgorithmResult
from whalepy.models.fitness_function import FitnessFunction, coerce_fitness_function
from whalepy.models.population import Population
from whalepy.models.stop_condition.never_stop_condition import NeverStopCondition
from whalepy.models.stop_condition.stop_condition import StopCondition
from whalepy.models.whale import Whale


class BaseWOAAlg(ABC):
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
        self.best_whale = self.population.get_best_whale(self.config.optimization_type)
        self.worst_whale = self.population.get_worst_whale(self.config.optimization_type)

    def _resolve_max_iter_reference(self) -> int:
        if self.config.max_iter is not None:
            return max(1, self.config.max_iter)
        if self.config.max_nfe is not None:
            remaining_evaluations = max(self.config.max_nfe - self.config.population_size, 0)
            estimated_iterations = math.ceil(remaining_evaluations / self.config.population_size)
            return max(1, estimated_iterations)
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
            message="Plain WOA finished.",
            epochs_completed=self.current_epoch,
            nfe=self.fitness_function.evaluations,
        )

    @abstractmethod
    def next_epoch(self) -> None:
        raise NotImplementedError


BaseWOA = BaseWOAAlg
