from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class Whale:
    position: list[float] = field(default_factory=list)
    fitness_value: Optional[float] = None
    lower_bounds: list[float] = field(default_factory=list)
    upper_bounds: list[float] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
