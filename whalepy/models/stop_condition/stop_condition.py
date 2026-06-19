from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    pass


class StopCondition(ABC):
    @abstractmethod
    def should_stop(self, algorithm: Any, best_whale: "Whale | None" = None) -> bool:
        raise NotImplementedError
