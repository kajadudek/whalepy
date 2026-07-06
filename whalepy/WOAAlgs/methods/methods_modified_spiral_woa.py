from __future__ import annotations

import math

from whalepy.WOAAlgs.methods.methods_woa import (
    encircle_best_whale,
    explore_random_whale,
    spiral_update,
)


def compute_logarithmic_spiral_step(
        whale_position: list[float],
        best_position: list[float],
        l_value: float,
        spiral_b: float,
) -> list[float]:
    return spiral_update(
        whale_position=whale_position,
        best_position=best_position,
        l_value=l_value,
        spiral_constant=spiral_b,
    )


def compute_archimedean_spiral_step(
        whale_position: list[float],
        best_position: list[float],
        l_value: float,
        progress_ratio: float,
        spiral_step: float,
        spiral_shrink_factor: float,
) -> list[float]:
    progress_ratio = min(max(progress_ratio, 0.0), 1.0)
    radial_term = spiral_step * abs(l_value) + spiral_shrink_factor * (1.0 - progress_ratio)
    return [
        abs(best_coordinate - coordinate)
        * radial_term
        * math.cos(2.0 * math.pi * l_value)
        + best_coordinate
        for coordinate, best_coordinate in zip(whale_position, best_position)
    ]


def apply_modified_spiral_update(
        whale_position: list[float],
        best_position: list[float],
        l_value: float,
        progress_ratio: float,
        spiral_mode: str,
        spiral_b: float,
        spiral_step: float,
        spiral_shrink_factor: float,
) -> list[float]:
    if spiral_mode == "logarithmic":
        return compute_logarithmic_spiral_step(
            whale_position=whale_position,
            best_position=best_position,
            l_value=l_value,
            spiral_b=spiral_b,
        )
    if spiral_mode == "archimedean":
        return compute_archimedean_spiral_step(
            whale_position=whale_position,
            best_position=best_position,
            l_value=l_value,
            progress_ratio=progress_ratio,
            spiral_step=spiral_step,
            spiral_shrink_factor=spiral_shrink_factor,
        )
    raise ValueError(f"Unsupported spiral mode: {spiral_mode}")


def update_one_modified_spiral_whale_position(
        whale_position: list[float],
        best_position: list[float],
        random_position: list[float],
        a_value: float,
        c_value: float,
        p_value: float,
        l_value: float,
        progress_ratio: float,
        spiral_mode: str,
        spiral_b: float,
        spiral_step: float,
        spiral_shrink_factor: float,
) -> list[float]:
    if p_value < 0.5:
        if abs(a_value) < 1.0:
            return encircle_best_whale(whale_position, best_position, a_value, c_value)
        return explore_random_whale(whale_position, random_position, a_value, c_value)
    return apply_modified_spiral_update(
        whale_position=whale_position,
        best_position=best_position,
        l_value=l_value,
        progress_ratio=progress_ratio,
        spiral_mode=spiral_mode,
        spiral_b=spiral_b,
        spiral_step=spiral_step,
        spiral_shrink_factor=spiral_shrink_factor,
    )
