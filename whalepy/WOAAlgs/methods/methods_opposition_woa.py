from __future__ import annotations


def compute_opposite_position(
        position: list[float],
        lb: list[float],
        ub: list[float],
) -> list[float]:
    return [
        float(lower_bound) + float(upper_bound) - float(value)
        for value, lower_bound, upper_bound in zip(position, lb, ub)
    ]
