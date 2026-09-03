from __future__ import annotations

import random


def single_dimensional_swimming(
        whale_position: list[float],
        best_position: list[float],
        a_value: float,
        c_value: float,
        rng: random.Random,
) -> tuple[list[float], int]:
    dimension_index = rng.randrange(len(whale_position))
    new_position = list(whale_position)

    best_coordinate = float(best_position[dimension_index])
    current_coordinate = float(whale_position[dimension_index])
    distance = abs(c_value * best_coordinate - current_coordinate)
    new_position[dimension_index] = best_coordinate - a_value * distance

    return new_position, dimension_index
