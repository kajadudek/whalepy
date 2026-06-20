from __future__ import annotations

from whalepy.WOAAlgs.base import BaseWOAAlg
from whalepy.WOAAlgs.methods.methods_cwoa import (
    chaotic_initialize_positions,
    chaotic_map_step,
    chaotic_value_to_index,
    chaotic_value_to_spiral_l,
    compute_chaotic_a,
    sanitize_chaotic_value,
    update_one_chaotic_whale_position,
)
from whalepy.WOAAlgs.methods.methods_woa import update_control_parameter
from whalepy.models.enums.boundary_constrain import repair_position
from whalepy.models.whale import Whale


class CWOA(BaseWOAAlg):
    def __init__(self, config, stop_condition=None) -> None:
        super().__init__(config, stop_condition=stop_condition)
        self.chaotic_state = sanitize_chaotic_value(config.chaotic_seed)

    def _advance_chaotic_state(self) -> float:
        self.chaotic_state = chaotic_map_step(
            value=self.chaotic_state,
            chaotic_map=self.config.chaotic_map,
            logistic_a=self.config.logistic_a,
            sine_a=self.config.sine_a,
        )
        return self.chaotic_state

    def _initialize(self) -> None:
        if self.config.max_nfe is not None and self.config.max_nfe < self.config.population_size:
            raise ValueError("max_nfe must be at least population_size for the initial evaluation.")

        if self.config.use_chaotic_initialization:
            positions, last_state = chaotic_initialize_positions(
                population_size=self.config.population_size,
                dimension=self.config.dimension,
                lb=self.config.lb,
                ub=self.config.ub,
                chaotic_seed=self.chaotic_state,
                chaotic_map=self.config.chaotic_map,
                logistic_a=self.config.logistic_a,
                sine_a=self.config.sine_a,
            )
            self.population.whales = [
                Whale(position=position, lb=self.config.lb, ub=self.config.ub)
                for position in positions
            ]
            self.population.epoch = 0
            self.chaotic_state = last_state
        else:
            self.population.initialize_whales(
                population_size=self.config.population_size,
                dimension=self.config.dimension,
                lb=self.config.lb,
                ub=self.config.ub,
                rng=self.rng,
            )

        self.population.update_fitness_values(self.fitness_function)
        self._refresh_population_state()
        if self.best_whale is not None and self.best_whale.fitness_value is not None:
            self.history = [self.best_whale.fitness_value]
        self.initialized = True

    def next_epoch(self) -> None:
        if self.best_whale is None:
            return

        a_base = update_control_parameter(self.current_epoch, self.max_iter_reference)
        if self.config.use_chaotic_a:
            a_base = compute_chaotic_a(a_base, self._advance_chaotic_state())

        best_reference = self.best_whale.copy()

        for index, whale in enumerate(self.population.whales):
            if self.config.max_nfe is not None and self.fitness_function.evaluations >= self.config.max_nfe:
                break

            chaotic_index_value = self._advance_chaotic_state()
            random_index = chaotic_value_to_index(chaotic_index_value, len(self.population.whales))
            if len(self.population.whales) > 1 and random_index == index:
                random_index = (random_index + 1) % len(self.population.whales)
            random_position = list(self.population.whales[random_index].position)

            if self.config.use_chaotic_coefficients:
                r1_value = self._advance_chaotic_state()
                r2_value = self._advance_chaotic_state()
            else:
                r1_value = self.rng.random()
                r2_value = self.rng.random()

            if self.config.use_chaotic_probability:
                p_value = self._advance_chaotic_state()
            else:
                p_value = self.rng.random()

            if self.config.use_chaotic_spiral:
                l_value = chaotic_value_to_spiral_l(self._advance_chaotic_state())
            else:
                l_value = self.rng.uniform(-1.0, 1.0)

            new_position = update_one_chaotic_whale_position(
                whale_position=whale.position,
                best_position=best_reference.position,
                random_position=random_position,
                a_base=a_base,
                r1_value=r1_value,
                r2_value=r2_value,
                p_value=p_value,
                l_value=l_value,
                spiral_constant=self.config.spiral_constant,
            )
            whale.position = repair_position(
                candidate=new_position,
                lb=self.config.lb,
                ub=self.config.ub,
                strategy=self.config.boundary_constraints_fun,
                rng=self.rng,
            )
            whale.lb = list(self.config.lb)
            whale.ub = list(self.config.ub)
            whale.metadata["index"] = index
            whale.metadata["chaotic_map"] = self.config.chaotic_map
            whale.metadata["chaotic_state"] = self.chaotic_state
            whale.fitness_value = self.fitness_function.evaluate(whale.position)

        self._refresh_population_state()
