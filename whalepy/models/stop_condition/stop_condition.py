from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    pass


class StopCondition(ABC):
    """
    Base class of user-defined stopping conditions.

    The algorithm calls :meth:`should_stop` after the initialization and after each
    iteration, and the run ends when it returns True.
    """

    @abstractmethod
    def should_stop(self, algorithm: Any, best_whale: "Whale | None" = None) -> bool:
        """
        Decides whether the run should be stopped.

        Parameters:
            algorithm: The running algorithm, which gives access to, e.g., ``current_epoch``,
                ``population`` and ``fitness_function.evaluations``.
            best_whale: Best solution found so far.

        Returns:
            bool: True if the run should be stopped.
        """
        raise NotImplementedError
