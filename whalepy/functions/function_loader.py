from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any, Callable


class FunctionLoader:
    def __init__(self, base_path: Path | None = None) -> None:
        self.base_path = base_path or Path(__file__).parent / "functions_info"

    def list_functions(self) -> list[str]:
        return sorted(path.stem for path in self.base_path.glob("*.json"))

    def load_metadata(self, name: str) -> dict[str, Any]:
        file_path = self.base_path / f"{name}.json"
        with file_path.open("r", encoding="ascii") as handle:
            return json.load(handle)

    def load_callable(self, name: str) -> Callable[[list[float]], float]:
        normalized_name = name.strip().lower()
        functions = {
            "ackley": ackley,
            "rastrigin": rastrigin,
            "rosenbrock": rosenbrock,
            "sphere": sphere,
        }
        if normalized_name not in functions:
            raise ValueError(f"Unknown benchmark function: {name}")
        return functions[normalized_name]


def sphere(candidate: list[float]) -> float:
    return sum(value * value for value in candidate)


def ackley(candidate: list[float]) -> float:
    dimension = len(candidate)
    if dimension == 0:
        return 0.0
    squared_sum = sum(value * value for value in candidate)
    cosine_sum = sum(math.cos(2.0 * math.pi * value) for value in candidate)
    term_1 = -20.0 * math.exp(-0.2 * math.sqrt(squared_sum / dimension))
    term_2 = -math.exp(cosine_sum / dimension)
    return term_1 + term_2 + 20.0 + math.e


def rastrigin(candidate: list[float]) -> float:
    return sum(value * value - 10.0 * math.cos(2.0 * math.pi * value) + 10.0 for value in candidate)


def rosenbrock(candidate: list[float]) -> float:
    if len(candidate) < 2:
        return 0.0
    total = 0.0
    for index in range(len(candidate) - 1):
        x_value = candidate[index]
        y_value = candidate[index + 1]
        total += 100.0 * (y_value - x_value ** 2) ** 2 + (1.0 - x_value) ** 2
    return total
