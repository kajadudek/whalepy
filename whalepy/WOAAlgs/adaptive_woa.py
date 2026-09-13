from whalepy.WOAAlgs.base import BaseWOAAlg
from whalepy.WOAAlgs.methods.methods_adaptive_woa import (
    compute_adaptive_inertia_weight,
    compute_adaptive_spiral_probability,
    compute_nonlinear_a,
    update_one_adaptive_whale_position,
)
from whalepy.models.enums.boundary_constrain import repair_position


class AdaptiveWOA(BaseWOAAlg):
    """
    AdaptiveWOA

    Links:
    https://indjst.org/articles/a-novel-adaptive-whale-optimization-algorithm-for-global-optimization
    https://www.sciencedirect.com/science/article/abs/pii/S0957417419307353
    https://link.springer.com/article/10.1007/s44196-022-00092-7

    References:
    Trivedi, I.N., Pradeep, J., Narottam, J., Arvind, K., Dilip, L., 2016.
    Novel Adaptive Whale Optimization Algorithm for Global Optimization.
    Indian Journal of Science and Technology 9.
    https://doi.org/10.17485/ijst/2016/v9i38/101939

    Chen, H., Yang, C., Heidari, A.A., Zhao, X., 2020.
    An efficient double adaptive random spare reinforced whale optimization
    algorithm. Expert Systems with Applications 154, 113018.
    https://doi.org/10.1016/j.eswa.2019.113018

    Sun, G., Shang, Y., Yuan, K., Gao, H., 2022.
    An Improved Whale Optimization Algorithm Based on Nonlinear Parameters
    and Feedback Mechanism. Int J Comput Intell Syst 15.
    https://doi.org/10.1007/s44196-022-00092-7
    """

    def next_epoch(self) -> None:
        if self.best_whale is None:
            return

        a_base = compute_nonlinear_a(
            epoch=self.current_epoch,
            max_iter=self.max_iter_reference,
            strategy=self.config.a_strategy,
        )
        inertia_weight = 1.0
        if self.config.use_inertia_weight:
            inertia_weight = compute_adaptive_inertia_weight(
                epoch=self.current_epoch,
                max_iter=self.max_iter_reference,
            )

        spiral_probability = 1.0 - self.config.encircling_probability
        if self.config.adaptive_probability:
            spiral_probability = compute_adaptive_spiral_probability(
                epoch=self.current_epoch,
                max_iter=self.max_iter_reference,
                p_start=self.config.p_start,
                p_end=self.config.p_end,
            )

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

            new_position = update_one_adaptive_whale_position(
                whale_position=whale.position,
                best_position=best_reference.position,
                random_position=random_position,
                a_value=a_value,
                c_value=c_value,
                p_value=p_value,
                l_value=l_value,
                spiral_constant=self.config.spiral_constant,
                inertia_weight=inertia_weight,
                spiral_probability=spiral_probability,
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
            whale.metadata["a_base"] = a_base
            whale.metadata["inertia_weight"] = inertia_weight
            whale.metadata["spiral_probability"] = spiral_probability
            whale.fitness_value = self.fitness_function.evaluate(whale.position)

        self._refresh_population_state()
