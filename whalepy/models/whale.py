from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class Whale:
    position: list[float] = field(default_factory=list)
    fitness_value: Optional[float] = None
    lb: list[float] = field(default_factory=list)
    ub: list[float] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.position = [float(value) for value in self.position]
        self.lb = [float(value) for value in self.lb]
        self.ub = [float(value) for value in self.ub]

    def copy(self) -> "Whale":
        return Whale(
            position=list(self.position),
            fitness_value=self.fitness_value,
            lb=list(self.lb),
            ub=list(self.ub),
            metadata=dict(self.metadata),
        )

    def __repr__(self) -> str:
        fitness_text = "None" if self.fitness_value is None else f"{self.fitness_value:.6f}"
        return f"Whale(position={self.position}, fitness_value={fitness_text})"
