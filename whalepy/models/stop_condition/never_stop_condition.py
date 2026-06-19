from __future__ import annotations

from typing import TYPE_CHECKING, Any

from whalepy.models.stop_condition.stop_condition import StopCondition

if TYPE_CHECKING:
    pass


class NeverStopCondition(StopCondition):
    def should_stop(self, algorithm: Any, best_whale: "Whale | None" = None) -> bool:
        return False
