# whalepy

`whalepy` is a research-oriented Python toolbox scaffold for the Whale Optimization Algorithm (WOA) family.

The project now includes a first working implementation of the plain/basic Whale Optimization Algorithm for
continuous benchmark functions.

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

Basic installation:

```bash
pip install .
```

## Usage

Minimal working usage:

```python
from whalepy import WOA
from whalepy.WOAAlgs.data import WOAData
from whalepy.functions.function_loader import FunctionLoader

loader = FunctionLoader()
config = WOAData(
    population_size=25,
    max_iter=80,
    max_nfe=2200,
    dimension=5,
    lb=[-5.0] * 5,
    ub=[5.0] * 5,
    function=loader.load_callable("sphere"),
    seed=7,
)

algorithm = WOA(config)
result = algorithm.run()
print(result.best_fitness_value)
```

If both `max_iter` and `max_nfe` are provided, the run stops when the first budget is exhausted.

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

Implemented now:

- plain/basic WOA
- built-in Sphere, Ackley, Rastrigin, and Rosenbrock benchmark callables
- WOA-specific `Whale` and `Population` models

Still placeholder:

- Adaptive WOA
- CWOA
- Modified Spiral Search WOA
- Mutation-Based WOA
- Random Walk WOA (Levy Flight)
