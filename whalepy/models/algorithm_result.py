from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from whalepy.models.whale import Whale


@dataclass
class AlgorithmResult:
    best_whale: Optional[Whale] = None
    worst_whale: Optional[Whale] = None
    best_fitness_value: Optional[float] = None
    worst_fitness_value: Optional[float] = None
    mean_fitness_value: Optional[float] = None
    std_fitness_value: Optional[float] = None
    history: list[float] = field(default_factory=list)
    success: bool = False
    message: str = ""
    epochs_completed: int = 0
    nfe: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)
