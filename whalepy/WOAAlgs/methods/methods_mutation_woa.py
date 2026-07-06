from __future__ import annotations

import random

from whalepy.WOAAlgs.methods.methods_woa import update_one_whale_position
from whalepy.models.enums.optimization import OptimizationType


def select_distinct_random_indices(
        population_size: int,
        excluded_index: int,
        rng: random.Random,
) -> tuple[int, int, int]:
    available_indices = [index for index in range(population_size) if index != excluded_index]
    if len(available_indices) < 3:
        raise ValueError("MutationWOA requires at least 4 whales for DE/rand/1 mutation.")
    selected = rng.sample(available_indices, 3)
    return selected[0], selected[1], selected[2]


def generate_de_rand_1_mutant(
        base_position: list[float],
        position_2: list[float],
        position_3: list[float],
        mutation_factor: float,
) -> list[float]:
    return [
        base_coordinate + mutation_factor * (coordinate_2 - coordinate_3)
        for base_coordinate, coordinate_2, coordinate_3 in zip(base_position, position_2, position_3)
    ]


def blend_candidates(
        woa_candidate: list[float],
        mutant_candidate: list[float],
        mixing_probability: float,
        rng: random.Random,
) -> list[float]:
    if mixing_probability <= 0.0:
        return list(woa_candidate)
    if mixing_probability >= 1.0:
        return list(mutant_candidate)
    return [
        mutant_value if rng.random() < mixing_probability else woa_value
        for woa_value, mutant_value in zip(woa_candidate, mutant_candidate)
    ]


def is_better_candidate(
        candidate_fitness: float,
        reference_fitness: float,
        optimization_type: OptimizationType,
) -> bool:
    if optimization_type == OptimizationType.MAXIMIZATION:
        return candidate_fitness > reference_fitness
    return candidate_fitness < reference_fitness


def select_candidate_position(
        woa_candidate: list[float],
        woa_fitness: float,
        mutation_candidate: list[float],
        mutation_fitness: float,
        optimization_type: OptimizationType,
        use_mutation_selection: bool,
) -> tuple[list[float], float]:
    if not use_mutation_selection:
        return mutation_candidate, mutation_fitness
    if is_better_candidate(mutation_fitness, woa_fitness, optimization_type):
        return mutation_candidate, mutation_fitness
    return woa_candidate, woa_fitness


def update_one_mutation_whale_position(
        whale_position: list[float],
        best_position: list[float],
        random_position: list[float],
        a_value: float,
        c_value: float,
        p_value: float,
        l_value: float,
        spiral_constant: float,
) -> list[float]:
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
