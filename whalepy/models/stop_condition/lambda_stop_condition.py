from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Callable

from whalepy.models.stop_condition.stop_condition import StopCondition

if TYPE_CHECKING:
    pass


@dataclass
class LambdaStopCondition(StopCondition):
    """
    Stopping condition defined by a function ``predicate(algorithm, best_whale) -> bool``.

    Because it is called after the initialization and after each iteration, it can also be
    used to record the state of the run.

    Example:
        >>> stop = LambdaStopCondition(lambda algorithm, best: best.fitness_value < 1e-6)
    """

    predicate: Callable[[Any, "Whale | None"], bool]

    def should_stop(self, algorithm: Any, best_whale: "Whale | None" = None) -> bool:
        return self.predicate(algorithm, best_whale)
