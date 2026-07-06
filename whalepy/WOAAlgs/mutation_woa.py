from __future__ import annotations

from whalepy.WOAAlgs.base import BaseWOAAlg
from whalepy.WOAAlgs.methods.methods_mutation_woa import (
    blend_candidates,
    generate_de_rand_1_mutant,
    select_candidate_position,
    select_distinct_random_indices,
    update_one_mutation_whale_position,
)
from whalepy.WOAAlgs.methods.methods_woa import update_control_parameter
from whalepy.models.enums.boundary_constrain import repair_position


class MutationWOA(BaseWOAAlg):
    def next_epoch(self) -> None:
        if self.best_whale is None:
            return

        a_base = update_control_parameter(self.current_epoch, self.max_iter_reference)
        best_reference = self.best_whale.copy()

        for index, whale in enumerate(self.population.whales):
            if self.config.max_nfe is not None and self.fitness_function.evaluations >= self.config.max_nfe:
                break

            random_whale = whale
            while len(self.population.whales) > 1 and random_whale is whale:
                random_whale = self.population.whales[self.rng.randrange(len(self.population.whales))]
            random_position = list(random_whale.position)

            r1 = self.rng.random()
            r2 = self.rng.random()
            a_value = 2.0 * a_base * r1 - a_base
            c_value = 2.0 * r2
            p_value = self.rng.random()
            l_value = self.rng.uniform(-1.0, 1.0)

            woa_candidate = update_one_mutation_whale_position(
                whale_position=whale.position,
                best_position=best_reference.position,
                random_position=random_position,
                a_value=a_value,
                c_value=c_value,
                p_value=p_value,
                l_value=l_value,
                spiral_constant=self.config.spiral_constant,
            )
            woa_candidate = repair_position(
                candidate=woa_candidate,
                lb=self.config.lb,
                ub=self.config.ub,
                strategy=self.config.boundary_constraints_fun,
                rng=self.rng,
            )
            woa_fitness = self.fitness_function.evaluate(woa_candidate)

            mutation_candidate = list(woa_candidate)
            mutation_fitness = woa_fitness

            if (
                    self.config.mutation_probability > 0.0
                    and self.rng.random() < self.config.mutation_probability
                    and len(self.population.whales) >= 4
            ):
                r_index_1, r_index_2, r_index_3 = select_distinct_random_indices(
                    population_size=len(self.population.whales),
                    excluded_index=index,
                    rng=self.rng,
                )
                base_position = self.population.whales[r_index_1].position
                position_2 = self.population.whales[r_index_2].position
                position_3 = self.population.whales[r_index_3].position
                raw_mutant = generate_de_rand_1_mutant(
                    base_position=base_position,
                    position_2=position_2,
                    position_3=position_3,
                    mutation_factor=self.config.mutation_factor,
                )
                mutation_candidate = blend_candidates(
                    woa_candidate=woa_candidate,
                    mutant_candidate=raw_mutant,
                    mixing_probability=self.config.mutation_probability,
                    rng=self.rng,
                )
                mutation_candidate = repair_position(
                    candidate=mutation_candidate,
                    lb=self.config.lb,
                    ub=self.config.ub,
                    strategy=self.config.boundary_constraints_fun,
                    rng=self.rng,
                )
                if self.config.max_nfe is not None and self.fitness_function.evaluations >= self.config.max_nfe:
                    selected_position = woa_candidate
                    selected_fitness = woa_fitness
                else:
                    mutation_fitness = self.fitness_function.evaluate(mutation_candidate)
                    selected_position, selected_fitness = select_candidate_position(
                        woa_candidate=woa_candidate,
                        woa_fitness=woa_fitness,
                        mutation_candidate=mutation_candidate,
                        mutation_fitness=mutation_fitness,
                        optimization_type=self.config.optimization_type,
                        use_mutation_selection=self.config.use_mutation_selection,
                    )
                whale.metadata["mutation_applied"] = True
            else:
                selected_position = woa_candidate
                selected_fitness = woa_fitness
                whale.metadata["mutation_applied"] = False

            whale.position = list(selected_position)
            whale.lb = list(self.config.lb)
            whale.ub = list(self.config.ub)
            whale.metadata["index"] = index
            whale.metadata["mutation_strategy"] = self.config.mutation_strategy
            whale.fitness_value = selected_fitness

        self._refresh_population_state()
