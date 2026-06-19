from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from typing import Optional

from whalepy.models.enums.optimization import OptimizationType
from whalepy.models.fitness_function import FitnessFunction
from whalepy.models.whale import Whale


@dataclass
class Population:
    whales: list[Whale] = field(default_factory=list)
    epoch: int = 0

    def initialize_whales(
            self,
            population_size: int,
            dimension: int,
            lb: list[float],
            ub: list[float],
            rng: random.Random,
    ) -> None:
        self.whales = []
        for _ in range(population_size):
            position = [rng.uniform(lb[i], ub[i]) for i in range(dimension)]
            self.whales.append(Whale(position=position, lb=lb, ub=ub))
        self.epoch = 0

    def update_fitness_values(
            self,
            fitness_function: FitnessFunction,
            max_evaluations: Optional[int] = None,
    ) -> int:
        evaluations_used = 0
        for whale in self.whales:
            if max_evaluations is not None and evaluations_used >= max_evaluations:
                break
            whale.fitness_value = fitness_function.evaluate(whale.position)
            evaluations_used += 1
        return evaluations_used

    def get_best_whale(
            self,
            optimization_type: OptimizationType = OptimizationType.MINIMIZATION,
    ) -> Optional[Whale]:
        comparable_whales = [whale for whale in self.whales if whale.fitness_value is not None]
        if not comparable_whales:
            return None
        if optimization_type == OptimizationType.MAXIMIZATION:
            return max(comparable_whales, key=lambda whale: whale.fitness_value).copy()
        return min(comparable_whales, key=lambda whale: whale.fitness_value).copy()

    def get_worst_whale(
            self,
            optimization_type: OptimizationType = OptimizationType.MINIMIZATION,
    ) -> Optional[Whale]:
        comparable_whales = [whale for whale in self.whales if whale.fitness_value is not None]
        if not comparable_whales:
            return None
        if optimization_type == OptimizationType.MAXIMIZATION:
            return min(comparable_whales, key=lambda whale: whale.fitness_value).copy()
        return max(comparable_whales, key=lambda whale: whale.fitness_value).copy()

    def mean_fitness(self) -> Optional[float]:
        values = [whale.fitness_value for whale in self.whales if whale.fitness_value is not None]
        if not values:
            return None
        return sum(values) / len(values)

    def std_fitness(self) -> Optional[float]:
        values = [whale.fitness_value for whale in self.whales if whale.fitness_value is not None]
        if not values:
            return None
        mean_value = sum(values) / len(values)
        variance = sum((value - mean_value) ** 2 for value in values) / len(values)
        return math.sqrt(variance)
