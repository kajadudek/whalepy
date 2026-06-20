from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Callable


class FitnessFunction(ABC):
    def __init__(self) -> None:
        self.evaluations = 0

    def __call__(self, candidate: Any) -> float:
        return self.evaluate(candidate)

    @abstractmethod
    def evaluate(self, candidate: Any) -> float:
        raise NotImplementedError

    def reset(self) -> None:
        self.evaluations = 0


class CallableFitnessFunction(FitnessFunction):
    def __init__(self, function: Callable[[Any], float], name: str = "callable_fitness"):
        super().__init__()
        self.function = function
        self.name = name

    def evaluate(self, candidate: Any) -> float:
        self.evaluations += 1
        return float(self.function(candidate))


class CountingFitnessFunction(FitnessFunction):
    def __init__(
            self,
            objective: Callable[[Any], float] | FitnessFunction,
            name: str = "counting_fitness",
    ) -> None:
        super().__init__()
        self.objective = objective
        self.name = name

    def evaluate(self, candidate: Any) -> float:
        self.evaluations += 1
        if isinstance(self.objective, FitnessFunction):
            return float(self.objective.evaluate(candidate))
        return float(self.objective(candidate))


class NamedFitnessFunction(FitnessFunction):
    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name

        from whalepy.functions.function_loader import FunctionLoader

        self.function = FunctionLoader().load_callable(name)

    def evaluate(self, candidate: Any) -> float:
        self.evaluations += 1
        return float(self.function(candidate))


def coerce_fitness_function(
        objective: Callable[[Any], float] | FitnessFunction | None,
) -> FitnessFunction:
    if objective is None:
        raise ValueError("A fitness function is required for WOA.")
    if isinstance(objective, FitnessFunction):
        return objective
    if callable(objective):
        return CountingFitnessFunction(objective, name=getattr(objective, "__name__", "objective"))
    raise TypeError("Unsupported fitness function type.")
