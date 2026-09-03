from __future__ import annotations

from whalepy.WOAAlgs.methods.methods_opposition_woa import compute_opposite_position
from whalepy.WOAAlgs.woa import WOA
from whalepy.models.enums.boundary_constrain import repair_position
from whalepy.models.enums.optimization import OptimizationType
from whalepy.models.whale import Whale


class OppositionBasedWOA(WOA):
    def initialization_nfe_cost(self) -> int:
        return 2 * int(self.config.population_size)

    def _initialize(self) -> None:
        if self.config.max_nfe is not None and self.config.max_nfe < 2*self.config.population_size:
            raise ValueError("max_nfe must be at least 2*population_size for the initial evaluation.")

        self.population.initialize_whales(
            population_size=self.config.population_size,
            dimension=self.config.dimension,
            lb=self.config.lb,
            ub=self.config.ub,
            rng=self.rng,
        )
        self.population.update_fitness_values(self.fitness_function)

        if self.config.use_obl_initialization:
            self._apply_obl_best_of_two_populations()

        self._refresh_population_state()
        if self.best_whale is not None and self.best_whale.fitness_value is not None:
            self.history = [self.best_whale.fitness_value]
        self.initialized = True

    def _apply_obl_best_of_two_populations(self) -> None:
        opposite_whales: list[Whale] = []
        for whale in self.population.whales:
            if whale.fitness_value is None:
                continue
            if self.config.max_nfe is not None and self.fitness_function.evaluations >= self.config.max_nfe:
                break
            opposite_position = compute_opposite_position(
                position=whale.position,
                lb=self.config.lb,
                ub=self.config.ub,
            )
            opposite_position = repair_position(
                candidate=opposite_position,
                lb=self.config.lb,
                ub=self.config.ub,
                strategy=self.config.boundary_constraints_fun,
                rng=self.rng,
            )
            opposite_fitness = self.fitness_function.evaluate(opposite_position)
            opposite_whale = Whale(
                position=list(opposite_position),
                fitness_value=opposite_fitness,
                lb=list(self.config.lb),
                ub=list(self.config.ub),
            )
            opposite_whale.metadata["origin"] = "obl_opposite"
            opposite_whales.append(opposite_whale)

        if not opposite_whales:
            return

        combined_pool = list(self.population.whales) + opposite_whales

        reverse_order = self.config.optimization_type == OptimizationType.MAXIMIZATION
        combined_pool.sort(key=self._fitness_sort_key, reverse=reverse_order)

        self.population.whales = combined_pool[: self.config.population_size]

    def _fitness_sort_key(self, whale: Whale) -> float:
        if whale.fitness_value is None:
            return float("-inf") if self.config.optimization_type == OptimizationType.MAXIMIZATION else float("inf")
        return whale.fitness_value
