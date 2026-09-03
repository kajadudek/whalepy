from __future__ import annotations

import random


def sample_gaussian_step(dimension: int, rng: random.Random) -> list[float]:
    return [rng.gauss(0.0, 1.0) for _ in range(dimension)]


def apply_gaussian_mutation(
        position: list[float],
        gaussian_steps: list[float],
) -> list[float]:
    return [
        float(coordinate) * (1.0 + float(step))
        for coordinate, step in zip(position, gaussian_steps)
    ]
