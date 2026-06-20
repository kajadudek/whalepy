from __future__ import annotations

import math

from whalepy.WOAAlgs.methods.methods_woa import update_one_whale_position


def sanitize_chaotic_value(value: float) -> float:
    epsilon = 1e-12
    return min(max(float(value), epsilon), 1.0 - epsilon)


def logistic_map_step(value: float, parameter: float = 4.0) -> float:
    value = sanitize_chaotic_value(value)
    return sanitize_chaotic_value(parameter * value * (1.0 - value))


def tent_map_step(value: float) -> float:
    value = sanitize_chaotic_value(value)
    if value < 0.7:
        return sanitize_chaotic_value(value / 0.7)
    return sanitize_chaotic_value(1.4286 * (1.0 - value))


def sine_map_step(value: float, parameter: float = 4.0) -> float:
    value = sanitize_chaotic_value(value)
    return sanitize_chaotic_value((parameter / 4.0) * math.sin(math.pi * value))


def chaotic_map_step(
        value: float,
        chaotic_map: str,
        logistic_a: float = 4.0,
        sine_a: float = 4.0,
) -> float:
    if chaotic_map == "logistic":
        return logistic_map_step(value, logistic_a)
    if chaotic_map == "tent":
        return tent_map_step(value)
    if chaotic_map == "sine":
        return sine_map_step(value, sine_a)
    raise ValueError(f"Unsupported chaotic map: {chaotic_map}")


def generate_chaotic_sequence(
        length: int,
        chaotic_seed: float,
        chaotic_map: str,
        logistic_a: float = 4.0,
        sine_a: float = 4.0,
) -> list[float]:
    values: list[float] = []
    state = sanitize_chaotic_value(chaotic_seed)
    for _ in range(length):
        state = chaotic_map_step(
            value=state,
            chaotic_map=chaotic_map,
            logistic_a=logistic_a,
            sine_a=sine_a,
        )
        values.append(state)
    return values


def chaotic_value_to_spiral_l(value: float) -> float:
    return 2.0 * sanitize_chaotic_value(value) - 1.0


def chaotic_value_to_index(value: float, size: int) -> int:
    if size <= 1:
        return 0
    scaled = int(sanitize_chaotic_value(value) * size)
    return min(max(scaled, 0), size - 1)


def chaotic_initialize_positions(
        population_size: int,
        dimension: int,
        lb: list[float],
        ub: list[float],
        chaotic_seed: float,
        chaotic_map: str,
        logistic_a: float = 4.0,
        sine_a: float = 4.0,
) -> tuple[list[list[float]], float]:
    sequence = generate_chaotic_sequence(
        length=population_size * dimension,
        chaotic_seed=chaotic_seed,
        chaotic_map=chaotic_map,
        logistic_a=logistic_a,
        sine_a=sine_a,
    )
    positions: list[list[float]] = []
    pointer = 0
    for _ in range(population_size):
        position = []
        for dim_index in range(dimension):
            value = sequence[pointer]
            pointer += 1
            lower_bound = lb[dim_index]
            upper_bound = ub[dim_index]
            position.append(lower_bound + value * (upper_bound - lower_bound))
        positions.append(position)
    return positions, sequence[-1]


def compute_chaotic_a(base_a: float, chaotic_value: float) -> float:
    return base_a * sanitize_chaotic_value(chaotic_value)


def update_one_chaotic_whale_position(
        whale_position: list[float],
        best_position: list[float],
        random_position: list[float],
        a_base: float,
        r1_value: float,
        r2_value: float,
        p_value: float,
        l_value: float,
        spiral_constant: float,
) -> list[float]:
    a_value = 2.0 * a_base * r1_value - a_base
    c_value = 2.0 * r2_value
    return update_one_whale_position(
        whale_position=whale_position,
        best_position=best_position,
        random_position=random_position,
        a_value=a_value,
        c_value=c_value,
        p_value=p_value,
        l_value=l_value,
        spiral_constant=spiral_constant,
    )
