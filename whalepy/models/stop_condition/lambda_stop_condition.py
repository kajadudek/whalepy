from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Callable

from whalepy.models.stop_condition.stop_condition import StopCondition

if TYPE_CHECKING:
    pass


@dataclass
class LambdaStopCondition(StopCondition):
    predicate: Callable[[Any, "Whale | None"], bool]

    def should_stop(self, algorithm: Any, best_whale: "Whale | None" = None) -> bool:
        return self.predicate(algorithm, best_whale)
