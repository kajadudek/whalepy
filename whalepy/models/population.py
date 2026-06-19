from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from whalepy.models.whale import Whale


@dataclass
class Population:
    whales: list[Whale] = field(default_factory=list)
    epoch: int = 0

    def initialize_whales(self) -> None:
        # TODO: initialize whale positions and initial fitness values.
        raise NotImplementedError("Population initialization is not implemented yet.")

    def get_best_whale(self) -> Optional[Whale]:
        # TODO: select the current best whale using the configured objective.
        raise NotImplementedError("Best whale retrieval is not implemented yet.")

    def update_fitness_values(self) -> None:
        # TODO: evaluate all whales against the configured objective function.
        raise NotImplementedError("Population fitness updates are not implemented yet.")
