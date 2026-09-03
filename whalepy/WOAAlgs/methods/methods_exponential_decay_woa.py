from __future__ import annotations

import math


def compute_exponential_a(
        epoch: int,
        max_iter: int,
        a_initial: float,
        a_final: float,
        k: float,
) -> float:
    if k <= 0.0:
        raise ValueError("k must be greater than 0.")

    if max_iter <= 1:
        return a_initial

    progress = min(max(epoch / (max_iter - 1), 0.0), 1.0)

    normalized_decay = (math.exp(progress ** k) - 1.0) / (math.e - 1.0)

    return a_initial - (a_initial - a_final) * normalized_decay
