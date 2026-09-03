from __future__ import annotations

from whalepy.WOAAlgs.methods.methods_gaussian_woa import (
    apply_gaussian_mutation,
    sample_gaussian_step,
)
from whalepy.WOAAlgs.methods.methods_mutation_woa import is_better_candidate
from whalepy.WOAAlgs.woa import WOA
from whalepy.models.enums.boundary_constrain import repair_position


class GaussianWOA(WOA):
    def epoch_nfe_cost(self) -> int:
        return 2 * int(self.config.population_size)

    def next_epoch(self) -> None:
        super().next_epoch()

        if self.best_whale is None:
            return

        for whale in self.population.whales:
            if self.config.max_nfe is not None and self.fitness_function.evaluations >= self.config.max_nfe:
                break
            if whale.fitness_value is None:
                continue

            gaussian_steps = sample_gaussian_step(
                dimension=self.config.dimension,
                rng=self.rng,
            )
            mutated_position = apply_gaussian_mutation(
                position=whale.position,
                gaussian_steps=gaussian_steps,
            )
            mutated_position = repair_position(
                candidate=mutated_position,
                lb=self.config.lb,
                ub=self.config.ub,
                strategy=self.config.boundary_constraints_fun,
                rng=self.rng,
            )
            mutated_fitness = self.fitness_function.evaluate(mutated_position)

            if is_better_candidate(
                    candidate_fitness=mutated_fitness,
                    reference_fitness=whale.fitness_value,
                    optimization_type=self.config.optimization_type,
            ):
                whale.position = mutated_position
                whale.fitness_value = mutated_fitness
                whale.metadata["gaussian_mutation_accepted"] = True
            else:
                whale.metadata["gaussian_mutation_accepted"] = False

        self._refresh_population_state()
