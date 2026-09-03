from __future__ import annotations

from whalepy.WOAAlgs.base import BaseWOAAlg
from whalepy.WOAAlgs.methods.methods_single_dimensional_woa import single_dimensional_swimming
from whalepy.WOAAlgs.methods.methods_woa import (
    explore_random_whale,
    spiral_update,
    update_control_parameter,
)
from whalepy.models.enums.boundary_constrain import repair_position


class SingleDimensionalWOA(BaseWOAAlg):
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

            updated_dimension = -1
            if p_value < 0.5:
                if abs(a_value) < 1.0:
                    new_position, updated_dimension = single_dimensional_swimming(
                        whale_position=whale.position,
                        best_position=best_reference.position,
                        a_value=a_value,
                        c_value=c_value,
                        rng=self.rng,
                    )
                else:
                    new_position = explore_random_whale(
                        whale_position=whale.position,
                        random_position=random_position,
                        a_value=a_value,
                        c_value=c_value,
                    )
            else:
                new_position = spiral_update(
                    whale_position=whale.position,
                    best_position=best_reference.position,
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
            whale.metadata["sds_dimension"] = updated_dimension
            whale.fitness_value = self.fitness_function.evaluate(whale.position)

        self._refresh_population_state()
