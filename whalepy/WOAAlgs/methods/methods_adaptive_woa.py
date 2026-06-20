from __future__ import annotations

import math

from whalepy.WOAAlgs.methods.methods_woa import (
    explore_random_whale,
    spiral_update,
)


def compute_nonlinear_a(epoch: int, max_iter: int, strategy: str) -> float:
    if max_iter <= 0:
        return 0.0

    progress = min(max(epoch / max_iter, 0.0), 1.0)
    if strategy == "cosine":
        return 2.0 * math.cos((math.pi / 2.0) * progress)
    if strategy == "logarithmic":
        return 2.0 - math.log10(1.0 + 9.0 * progress)
    raise ValueError(f"Unsupported adaptive a strategy: {strategy}")


def compute_adaptive_inertia_weight(epoch: int, max_iter: int) -> float:
    if max_iter <= 0:
        return 1.0
    progress = min(max(epoch / max_iter, 0.0), 1.0)
    return 0.5 + 0.5 * progress


def compute_adaptive_spiral_probability(
        epoch: int,
        max_iter: int,
        p_start: float,
        p_end: float,
) -> float:
    if max_iter <= 0:
        return p_end
    progress = min(max(epoch / max_iter, 0.0), 1.0)
    return p_start + (p_end - p_start) * progress


def adaptive_encircle_best_whale(
        whale_position: list[float],
        best_position: list[float],
        a_value: float,
        c_value: float,
        inertia_weight: float,
) -> list[float]:
    return [
        inertia_weight * best_coordinate
        - a_value * abs(c_value * best_coordinate - coordinate)
        for coordinate, best_coordinate in zip(whale_position, best_position)
    ]


def update_one_adaptive_whale_position(
        whale_position: list[float],
        best_position: list[float],
        random_position: list[float],
        a_value: float,
        c_value: float,
        p_value: float,
        l_value: float,
        spiral_constant: float,
        inertia_weight: float,
        spiral_probability: float,
) -> list[float]:
    if p_value < spiral_probability:
        return spiral_update(whale_position, best_position, l_value, spiral_constant)
    if abs(a_value) < 1.0:
        return adaptive_encircle_best_whale(
            whale_position,
            best_position,
            a_value,
            c_value,
            inertia_weight,
        )
    return explore_random_whale(whale_position, random_position, a_value, c_value)
