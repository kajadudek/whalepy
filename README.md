# whalepy

`whalepy` is a research-oriented Python toolbox for the Whale Optimization Algorithm (WOA) family.

The project now includes working implementations of plain/basic WOA, Adaptive WOA, Chaotic WOA,
Mutation-Based WOA, Modified Spiral WOA, and Levy Walk WOA for continuous benchmark functions.

The scaffold uses a WOA-specific domain model built around `Whale` objects rather than generic evolutionary
abstractions.

Adaptive WOA extends the plain WOA loop with adaptive control schedules. In this project, the adaptive variant
supports nonlinear decay of the convergence coefficient `a`, an optional inertia-like weight in the leader
attraction step, and an optional adaptive spiral probability that increasingly favors exploitation later in the
run.

Chaotic WOA replaces selected random draws in WOA with deterministic chaotic sequences. In this project, the
chaotic variant supports logistic, tent, and sine maps, optional chaotic population initialization, chaotic
coefficient generation, chaotic branch probability, chaotic spiral values, and optional chaotic modulation of
the convergence coefficient `a`.

Modified Spiral WOA keeps the standard WOA exploration behavior and changes only the exploitation spiral around
the best whale. In this project, the variant supports both the standard logarithmic spiral and a practical
Archimedean-style spiral that shrinks more gradually and covers the local neighborhood more evenly.

Mutation-Based WOA augments the standard WOA movement with DE-inspired mutation. In this project, the mutation
variant keeps the normal WOA candidate, optionally creates a mutation candidate with `DE/rand/1`, evaluates both,
and keeps the better one according to the optimization mode.

Levy Walk WOA modifies the exploration phase with Levy-flight-based random walks. In this project, the Levy
variant uses Mantegna-style heavy-tailed steps during exploration while keeping standard WOA-like exploitation
around the best whale.

## Installation

Basic installation:

```bash
pip install .
```

## Usage

Common usage pattern:

```python
config = VariantData(...)
algorithm = Variant(config)
result = algorithm.run()
```

Top-level imports are available for all implemented variants:

```python
from whalepy import (
    AdaptiveWOA,
    AdaptiveWOAData,
    BoundaryConstraint,
    CWOA,
    CWOAData,
    FunctionLoader,
    LevyWalkWOA,
    LevyWalkWOAData,
    ModifiedSpiralWOA,
    ModifiedSpiralWOAData,
    MutationWOA,
    MutationWOAData,
    OptimizationType,
    WOA,
    WOAData,
    run_algorithm,
)
```

Basic WOA example:

```python
from whalepy import FunctionLoader, WOA, WOAData

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

Stopping rule:

- `max_iter` is the primary loop budget
- `max_nfe` is an additional evaluation cap
- if both are provided, the algorithm stops when either limit is reached first

Function handling:

- use `FunctionLoader().load_callable("sphere")` for built-in benchmarks
- or pass a plain Python callable with `function=my_objective`

Boundary handling:

- all variants accept `boundary_constraints_fun`
- built-in choices include `BoundaryConstraint.CLIP`, `BoundaryConstraint.REFLECT`, and
  `BoundaryConstraint.RANDOM_RESET`

Adaptive WOA usage:

```python
from whalepy import AdaptiveWOA, AdaptiveWOAData, FunctionLoader

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

Chaotic WOA usage:

```python
from whalepy import CWOA, CWOAData, FunctionLoader

loader = FunctionLoader()
config = CWOAData(
    population_size=25,
    max_iter=100,
    max_nfe=2600,
    dimension=5,
    lb=[-5.0] * 5,
    ub=[5.0] * 5,
    function=loader.load_callable("ackley"),
    seed=7,
    chaotic_map="logistic",
    chaotic_seed=0.37,
    use_chaotic_initialization=True,
    use_chaotic_probability=True,
    use_chaotic_coefficients=True,
    use_chaotic_spiral=True,
)

result = CWOA(config).run()
print(result.best_fitness_value)
```

Chaotic WOA notes:

- `chaotic_map="logistic"` uses the logistic map with `logistic_a=4.0` by default
- `chaotic_map="tent"` uses the tent map with the built-in `0.7 / 1.4286` schedule
- `chaotic_map="sine"` uses the sine map with `sine_a=4.0` by default
- chaotic values can replace standard random draws for initialization, `r`, `p`, and `l`
- `use_chaotic_a=True` optionally modulates the base convergence coefficient with chaos

Mutation-Based WOA usage:

```python
from whalepy import FunctionLoader, MutationWOA, MutationWOAData

loader = FunctionLoader()
config = MutationWOAData(
    population_size=30,
    max_iter=100,
    max_nfe=3500,
    dimension=5,
    lb=[-5.0] * 5,
    ub=[5.0] * 5,
    function=loader.load_callable("rastrigin"),
    seed=7,
    mutation_strategy="de_rand_1",
    mutation_factor=0.6,
    mutation_probability=0.35,
    use_mutation_selection=True,
)

result = MutationWOA(config).run()
print(result.best_fitness_value)
```

Modified Spiral WOA usage:

```python
from whalepy import FunctionLoader, ModifiedSpiralWOA, ModifiedSpiralWOAData

loader = FunctionLoader()
config = ModifiedSpiralWOAData(
    population_size=30,
    max_iter=120,
    max_nfe=3800,
    dimension=5,
    lb=[-5.0] * 5,
    ub=[5.0] * 5,
    function=loader.load_callable("ackley"),
    seed=7,
    spiral_mode="archimedean",
    spiral_b=1.0,
    spiral_step=0.25,
    spiral_shrink_factor=0.75,
)

result = ModifiedSpiralWOA(config).run()
print(result.best_fitness_value)
```

Levy Walk WOA usage:

```python
from whalepy import FunctionLoader, LevyWalkWOA, LevyWalkWOAData

loader = FunctionLoader()
config = LevyWalkWOAData(
    population_size=30,
    max_iter=120,
    max_nfe=3800,
    dimension=5,
    lb=[-5.0] * 5,
    ub=[5.0] * 5,
    function=loader.load_callable("ackley"),
    seed=7,
    levy_beta=1.5,
    levy_scale=0.05,
    use_levy_exploration=True,
    levy_mode="exploration_only",
)

result = LevyWalkWOA(config).run()
print(result.best_fitness_value)
```

Levy Walk WOA notes:

- `levy_beta` controls the heaviness of the Levy tail
- `levy_scale` controls the overall exploration step size
- `use_levy_exploration=True` enables Levy-flight exploration when `|A| >= 1`
- `levy_mode="exploration_only"` uses only the Levy move in the exploration branch
- `levy_mode="hybrid"` blends a standard WOA exploration candidate with a Levy-flight perturbation

Optional convenience helper:

```python
from whalepy import WOA, WOAData, run_algorithm

result = run_algorithm(WOA, WOAData(...))
```

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
- chaotic WOA with logistic, tent, and sine maps plus optional chaotic initialization and parameter draws
- mutation-based WOA with DE/rand/1 candidate generation and fitness-based selection
- modified spiral WOA with configurable logarithmic and Archimedean-style exploitation spirals
- Levy walk WOA with Levy-flight exploration using Mantegna's algorithm
- built-in Sphere, Ackley, Rastrigin, and Rosenbrock benchmark callables
- WOA-specific `Whale` and `Population` models
