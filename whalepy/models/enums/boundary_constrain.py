from __future__ import annotations

from enum import Enum
from typing import Any


class BoundaryConstraint(str, Enum):
    CLIP = "clip"
    REFLECT = "reflect"
    RANDOM_RESET = "random_reset"
    NONE = "none"


def repair_by_clipping(candidate: Any, lb: Any, ub: Any) -> Any:
    # TODO: implement clipping-based repair.
    raise NotImplementedError("Clipping repair is not implemented yet.")


def repair_by_reflection(candidate: Any, lb: Any, ub: Any) -> Any:
    # TODO: implement reflection-based repair.
    raise NotImplementedError("Reflection repair is not implemented yet.")


def repair_by_random_reset(candidate: Any, lb: Any, ub: Any) -> Any:
    # TODO: implement random-reset repair.
    raise NotImplementedError("Random-reset repair is not implemented yet.")
