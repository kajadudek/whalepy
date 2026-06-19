from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Callable


class FitnessFunction(ABC):
    @abstractmethod
    def evaluate(self, candidate: Any) -> float:
        raise NotImplementedError


@dataclass
class CallableFitnessFunction(FitnessFunction):
    function: Callable[[Any], float]
    name: str = "callable_fitness"

    def evaluate(self, candidate: Any) -> float:
        return self.function(candidate)


@dataclass
class NamedFitnessFunction(FitnessFunction):
    name: str

    def evaluate(self, candidate: Any) -> float:
        # TODO: connect this wrapper to the benchmark registry.
        raise NotImplementedError("Named fitness functions are not implemented yet.")
