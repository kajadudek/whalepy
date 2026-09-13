from __future__ import annotations

from typing import Any

from whalepy.models.algorithm_result import AlgorithmResult
from whalepy.models.enums.optimization import OptimizationType


class MetricHelper:
    """Helper functions for summarizing the results of a WOA run."""

    @staticmethod
    def summarize_history(
            history: list[float],
            optimization_type: OptimizationType = OptimizationType.MINIMIZATION,
    ) -> dict[str, Any]:
        """Returns the initial, final and best value of a convergence history."""
        if not history:
            raise ValueError("The history is empty.")
        if optimization_type == OptimizationType.MAXIMIZATION:
            best_value = max(history)
        else:
            best_value = min(history)
        return {
            "initial": history[0],
            "final": history[-1],
            "best": best_value,
            "iterations": len(history) - 1,
        }

    @staticmethod
    def summarize_best_whale(result: AlgorithmResult) -> dict[str, Any]:
        """Returns the position and fitness of the best whale together with the run statistics."""
        if result.best_whale is None:
            raise ValueError("The result does not contain a best whale.")
        return {
            "position": list(result.best_whale.position),
            "fitness": result.best_whale.fitness_value,
            "epochs_completed": result.epochs_completed,
            "nfe": result.nfe,
        }
