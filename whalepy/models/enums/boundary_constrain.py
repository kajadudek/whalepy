from __future__ import annotations

import random
from enum import Enum
from typing import Any, Callable


class BoundaryConstraint(str, Enum):
    CLIP = "clip"
    REFLECT = "reflect"
    RANDOM_RESET = "random_reset"
    NONE = "none"


def repair_by_clipping(candidate: Any, lb: Any, ub: Any) -> Any:
    return [
        min(max(float(value), float(lower_bound)), float(upper_bound))
        for value, lower_bound, upper_bound in zip(candidate, lb, ub)
    ]


def repair_by_reflection(candidate: Any, lb: Any, ub: Any) -> Any:
    repaired = []
    for value, lower_bound, upper_bound in zip(candidate, lb, ub):
        lower_bound = float(lower_bound)
        upper_bound = float(upper_bound)
        reflected = float(value)
        while reflected < lower_bound or reflected > upper_bound:
            if reflected < lower_bound:
                reflected = lower_bound + (lower_bound - reflected)
            if reflected > upper_bound:
                reflected = upper_bound - (reflected - upper_bound)
        repaired.append(reflected)
    return repaired


def repair_by_random_reset(
        candidate: Any,
        lb: Any,
        ub: Any,
        rng: random.Random | None = None,
) -> Any:
    rng = rng or random.Random()
    repaired = []
    for value, lower_bound, upper_bound in zip(candidate, lb, ub):
        lower_bound = float(lower_bound)
        upper_bound = float(upper_bound)
        if lower_bound <= float(value) <= upper_bound:
            repaired.append(float(value))
        else:
            repaired.append(rng.uniform(lower_bound, upper_bound))
    return repaired


def repair_position(
        candidate: Any,
        lb: Any,
        ub: Any,
        strategy: BoundaryConstraint | str | Callable[..., Any] = BoundaryConstraint.CLIP,
        rng: random.Random | None = None,
) -> Any:
    if callable(strategy) and not isinstance(strategy, BoundaryConstraint):
        return strategy(candidate, lb, ub)

    if strategy == BoundaryConstraint.NONE or strategy == "none":
        return [float(value) for value in candidate]
    if strategy == BoundaryConstraint.CLIP or strategy == "clip":
        return repair_by_clipping(candidate, lb, ub)
    if strategy == BoundaryConstraint.REFLECT or strategy == "reflect":
        return repair_by_reflection(candidate, lb, ub)
    if strategy == BoundaryConstraint.RANDOM_RESET or strategy == "random_reset":
        return repair_by_random_reset(candidate, lb, ub, rng=rng)

    raise ValueError(f"Unsupported boundary strategy: {strategy}")
