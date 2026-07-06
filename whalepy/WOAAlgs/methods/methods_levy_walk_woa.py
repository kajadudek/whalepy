from __future__ import annotations

import math
import random

from whalepy.WOAAlgs.methods.methods_woa import (
    encircle_best_whale,
    explore_random_whale,
    spiral_update,
)


def mantegna_sigma_u(beta: float) -> float:
    numerator = math.gamma(1.0 + beta) * math.sin(math.pi * beta / 2.0)
    denominator = math.gamma((1.0 + beta) / 2.0) * beta * (2.0 ** ((beta - 1.0) / 2.0))
    return (numerator / denominator) ** (1.0 / beta)


def sample_levy_walk_step(
        dimension: int,
        beta: float,
        rng: random.Random,
) -> list[float]:
    sigma_u = mantegna_sigma_u(beta)
    steps: list[float] = []
    for _ in range(dimension):
        u_value = rng.gauss(0.0, sigma_u)
        v_value = rng.gauss(0.0, 1.0)
        denominator = max(abs(v_value) ** (1.0 / beta), 1e-12)
        steps.append(u_value / denominator)
    return steps


def apply_levy_perturbation(
        whale_position: list[float],
        random_position: list[float],
        levy_steps: list[float],
        a_value: float,
        levy_scale: float,
) -> list[float]:
    return [
        coordinate + levy_scale * step * a_value * (coordinate - random_coordinate)
        for coordinate, random_coordinate, step in zip(whale_position, random_position, levy_steps)
    ]


def apply_random_walk_update(
        whale_position: list[float],
        random_position: list[float],
        a_value: float,
        c_value: float,
        levy_steps: list[float],
        levy_scale: float,
        levy_mode: str,
) -> list[float]:
    levy_candidate = apply_levy_perturbation(
        whale_position=whale_position,
        random_position=random_position,
        levy_steps=levy_steps,
        a_value=a_value,
        levy_scale=levy_scale,
    )
    if levy_mode == "exploration_only":
        return levy_candidate
    standard_candidate = explore_random_whale(
        whale_position=whale_position,
        random_position=random_position,
        a_value=a_value,
        c_value=c_value,
    )
    return [
        0.5 * (standard_value + levy_value)
        for standard_value, levy_value in zip(standard_candidate, levy_candidate)
    ]


def update_one_levy_walk_position(
        whale_position: list[float],
        best_position: list[float],
        random_position: list[float],
        a_value: float,
        c_value: float,
        p_value: float,
        l_value: float,
        spiral_constant: float,
        levy_steps: list[float],
        levy_scale: float,
        levy_mode: str,
        use_levy_exploration: bool,
) -> list[float]:
    if p_value < 0.5:
        if abs(a_value) < 1.0:
            return encircle_best_whale(whale_position, best_position, a_value, c_value)
        if use_levy_exploration:
            return apply_random_walk_update(
                whale_position=whale_position,
                random_position=random_position,
                a_value=a_value,
                c_value=c_value,
                levy_steps=levy_steps,
                levy_scale=levy_scale,
                levy_mode=levy_mode,
            )
        return explore_random_whale(whale_position, random_position, a_value, c_value)
    return spiral_update(whale_position, best_position, l_value, spiral_constant)
