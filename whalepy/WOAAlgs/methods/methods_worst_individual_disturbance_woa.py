from __future__ import annotations


def worst_individual_disturbance_update(
        whale_position: list[float],
        best_position: list[float],
        worst_position: list[float],
        a_value: float,
        c_value: float,
        r4: float,
) -> list[float]:
    disturbance_weight = 1.0 - float(r4)
    return [
        float(r4) * best_coordinate
        - a_value * abs(c_value * best_coordinate - coordinate)
        + disturbance_weight * worst_coordinate
        for coordinate, best_coordinate, worst_coordinate in zip(
            whale_position, best_position, worst_position
        )
    ]
