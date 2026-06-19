# whalepy

`whalepy` is a research-oriented Python toolbox scaffold for the Whale Optimization Algorithm (WOA) family.

This repository is currently a skeleton only. It provides package structure, placeholder classes, documentation stubs,
and example stubs for future implementation work.

The scaffold uses a WOA-specific domain model built around `Whale` objects rather than generic evolutionary
abstractions.

## Planned Variants

- WOA
- Adaptive WOA
- CWOA
- Modified Spiral Search WOA
- Mutation-Based WOA
- Random Walk WOA (Levy Flight)

## Installation

Placeholder installation flow:

```bash
pip install .
```

TODO: finalize packaging details and dependency list.

## Usage

Placeholder future usage:

```python
from whalepy import WOA
from whalepy.WOAAlgs.data import WOAData

config = WOAData(
    population_size=30,
    max_nfe=1000,
    dimension=10,
    lb=[-5.0] * 10,
    ub=[5.0] * 10,
)

algorithm = WOA(config)
```

The runtime behavior is not implemented yet.

## Project Layout

```text
whalepy/
  WOAAlgs/
  models/
  functions/
  helpers/
examples/
doc/
```

## Status

This project is intentionally scaffold-only at the moment. Real optimization logic, benchmark execution, plotting,
persistence, and algorithm-specific movement rules will be added later.
