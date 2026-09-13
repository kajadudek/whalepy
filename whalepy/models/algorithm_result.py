from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from whalepy.models.whale import Whale


@dataclass
class AlgorithmResult:
    """
    Result of a run returned by the ``run()`` method.

    Attributes:
        best_whale: Best solution found during the run (position and fitness value).
        worst_whale: Worst whale in the final population.
        best_fitness_value: Fitness value of the best solution found.
        worst_fitness_value: Fitness value of the worst whale in the final population.
        mean_fitness_value: Mean fitness value in the final population.
        std_fitness_value: Standard deviation of the fitness values in the final population.
        history: Best fitness value found so far after the initialization and after each
            iteration, which can be used to plot the convergence curve.
        success: True if a solution was found.
        message: Short description of the run.
        epochs_completed: Number of completed iterations.
        nfe: Number of objective function evaluations.
        metadata: Additional information about the run.
    """

    best_whale: Optional[Whale] = None
    worst_whale: Optional[Whale] = None
    best_fitness_value: Optional[float] = None
    worst_fitness_value: Optional[float] = None
    mean_fitness_value: Optional[float] = None
    std_fitness_value: Optional[float] = None
    history: list[float] = field(default_factory=list)
    success: bool = False
    message: str = ""
    epochs_completed: int = 0
    nfe: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)
