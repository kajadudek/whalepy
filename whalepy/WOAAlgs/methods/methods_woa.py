from __future__ import annotations

import math


def update_control_parameter(epoch: int, max_iter: int) -> float:
    if max_iter <= 1:
        return 2.0
    progress = min(max(epoch / (max_iter - 1), 0.0), 1.0)
    return 2.0 - 2.0 * progress


def encircle_best_whale(
        whale_position: list[float],
        best_position: list[float],
        a_value: float,
        c_value: float,
) -> list[float]:
    return [
        best_coordinate - a_value * abs(c_value * best_coordinate - coordinate)
        for coordinate, best_coordinate in zip(whale_position, best_position)
    ]


def explore_random_whale(
        whale_position: list[float],
        random_position: list[float],
        a_value: float,
        c_value: float,
) -> list[float]:
    return [
        random_coordinate - a_value * abs(c_value * random_coordinate - coordinate)
        for coordinate, random_coordinate in zip(whale_position, random_position)
    ]


def spiral_update(
        whale_position: list[float],
        best_position: list[float],
        l_value: float,
        spiral_constant: float,
) -> list[float]:
    return [
        abs(best_coordinate - coordinate)
        * math.exp(spiral_constant * l_value)
        * math.cos(2.0 * math.pi * l_value)
        + best_coordinate
        for coordinate, best_coordinate in zip(whale_position, best_position)
    ]


def update_one_whale_position(
        whale_position: list[float],
        best_position: list[float],
        random_position: list[float],
        a_value: float,
        c_value: float,
        p_value: float,
        l_value: float,
        spiral_constant: float,
) -> list[float]:
    if p_value < 0.5:
        if abs(a_value) < 1.0:
            return encircle_best_whale(whale_position, best_position, a_value, c_value)
        return explore_random_whale(whale_position, random_position, a_value, c_value)
    return spiral_update(whale_position, best_position, l_value, spiral_constant)
