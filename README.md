# whalepy

`whalepy` is a research-oriented Python toolbox for the Whale Optimization Algorithm (WOA) family.

The project now includes working implementations of plain/basic WOA, Adaptive WOA, Chaotic WOA, and
Mutation-Based WOA for continuous benchmark functions.

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

Mutation-Based WOA augments the standard WOA movement with DE-inspired mutation. In this project, the mutation
variant keeps the normal WOA candidate, optionally creates a mutation candidate with `DE/rand/1`, evaluates both,
and keeps the better one according to the optimization mode.

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

Chaotic WOA usage:

```python
from whalepy import CWOA
from whalepy.WOAAlgs.data import CWOAData
from whalepy.functions.function_loader import FunctionLoader

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
from whalepy import MutationWOA
from whalepy.WOAAlgs.data import MutationWOAData
from whalepy.functions.function_loader import FunctionLoader

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

Mutation-Based WOA notes:

- `mutation_strategy="de_rand_1"` uses `V_i = X_r1 + F * (X_r2 - X_r3)`
- `mutation_factor` is the DE scaling factor `F`
- `mutation_probability` controls how often mutation is attempted and how strongly the mutant is mixed in
- `use_mutation_selection=True` keeps the better result between the normal WOA candidate and the mutation candidate

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
- built-in Sphere, Ackley, Rastrigin, and Rosenbrock benchmark callables
- WOA-specific `Whale` and `Population` models

Still placeholder:

- Modified Spiral Search WOA
- Random Walk WOA (Levy Flight)
