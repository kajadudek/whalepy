from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from whalepy.models.whale import Whale


@dataclass
class AlgorithmResult:
    best_whale: Optional[Whale] = None
    worst_whale: Optional[Whale] = None
    history: list[float] = field(default_factory=list)
    success: bool = False
    message: str = ""
    epochs_completed: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)
