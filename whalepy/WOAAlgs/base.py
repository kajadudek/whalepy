from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from whalepy.WOAAlgs.data.alg_data import BaseData
from whalepy.models.algorithm_result import AlgorithmResult
from whalepy.models.population import Population
from whalepy.models.stop_condition.never_stop_condition import NeverStopCondition
from whalepy.models.stop_condition.stop_condition import StopCondition


class BaseWOAAlg(ABC):
    def __init__(
            self,
            config: BaseData,
            stop_condition: Optional[StopCondition] = None,
    ) -> None:
        self.config = config
        self.stop_condition = stop_condition or NeverStopCondition()
        self.population = Population()
        self.best_whale = None
        self.current_epoch = 0
        self.initialized = False

    def _initialize(self) -> None:
        # TODO: create whales, evaluate fitness values, and initialize trackers.
        self.initialized = True

    def run(self) -> AlgorithmResult:
        if not self.initialized:
            self._initialize()

        # TODO: replace this placeholder flow with a real optimization loop.
        result = AlgorithmResult(
            best_whale=None,
            worst_whale=None,
            history=[],
            success=False,
            message="WOA scaffold only. Optimization logic is not implemented yet.",
            epochs_completed=self.current_epoch,
        )
        return result

    @abstractmethod
    def next_epoch(self) -> None:
        raise NotImplementedError


BaseWOA = BaseWOAAlg
