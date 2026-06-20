# whalepy

`whalepy` is a research-oriented Python toolbox scaffold for the Whale Optimization Algorithm (WOA) family.

The project now includes working implementations of plain/basic WOA and Adaptive WOA for continuous
benchmark functions.

The scaffold uses a WOA-specific domain model built around `Whale` objects rather than generic evolutionary
abstractions.

Adaptive WOA extends the plain WOA loop with adaptive control schedules. In this project, the adaptive variant
supports nonlinear decay of the convergence coefficient `a`, an optional inertia-like weight in the leader
attraction step, and an optional adaptive spiral probability that increasingly favors exploitation later in the
run.

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

Adaptive WOA usage:

```python
from whalepy import AdaptiveWOA
from whalepy.WOAAlgs.data import AdaptiveWOAData
from whalepy.functions.function_loader import FunctionLoader

loader = FunctionLoader()
config = AdaptiveWOAData(
    population_size=25,
    max_iter=80,
    max_nfe=2200,
    dimension=5,
    lb=[-5.0] * 5,
    ub=[5.0] * 5,
    function=loader.load_callable("ackley"),
    seed=7,
    a_strategy="cosine",
    use_inertia_weight=True,
    adaptive_probability=True,
    p_start=0.5,
    p_end=0.9,
)

result = AdaptiveWOA(config).run()
print(result.best_fitness_value)
```

Adaptive WOA notes:

- `a_strategy="cosine"` uses a cosine decay for the convergence coefficient
- `a_strategy="logarithmic"` uses a logarithmic decay for the convergence coefficient
- `use_inertia_weight=True` enables a growing weight on the best-whale attraction term
- `adaptive_probability=True` gradually shifts more updates toward the spiral exploitation branch

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
- adaptive WOA with nonlinear `a`, adaptive inertia weight, and optional adaptive spiral probability
- built-in Sphere, Ackley, Rastrigin, and Rosenbrock benchmark callables
- WOA-specific `Whale` and `Population` models

Still placeholder:

- CWOA
- Modified Spiral Search WOA
- Mutation-Based WOA
- Random Walk WOA (Levy Flight)
