# whalepy

`whalepy` is a research-oriented Python toolbox for the Whale Optimization Algorithm (WOA) family.

The project now includes working implementations of plain/basic WOA, Adaptive WOA, Chaotic WOA,
Mutation-Based WOA, Modified Spiral WOA, Levy Walk WOA, Gaussian Mutation WOA, Opposition-Based
WOA, Single-Dimensional WOA, Worst-Individual-Disturbance WOA, and Exponential Decay WOA for
continuous benchmark problems.

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

Gaussian Mutation WOA (GM-WOA) runs the standard WOA update unchanged, then applies a multiplicative
Gaussian mutation `X' = X^A * (1 + G)` (element-wise) with `G ~ N(0, I)` to every whale, where `X^A` is
the position produced by the base WOA step. The mutated candidate replaces the current position only if it
improves the fitness (greedy selection). Because the perturbation is proportional to `|X^A_i|`, coordinates
near zero are barely changed while coordinates far from the origin can move substantially. Implementation
follows Luo et al. (2019).

Opposition-Based WOA reuses the base WOA main loop unchanged and only modifies population initialization.
A random population of size N is generated, an opposite candidate `x_opp = lb + ub - x` is produced for
each whale, both sets are evaluated, and the best N individuals from the resulting pool of 2N candidates
form the starting population.

Single-Dimensional WOA replaces the classical encircling-prey step with the single-dimensional swimming
mechanism from Du et al. (2020). Instead of updating the full position vector, a single randomly
selected coordinate `d` is updated via `X_d(t+1) = X*_d(t) - A * |C * X*_d(t) - X_d(t)|`, while all
other coordinates stay unchanged. The exploration branch and the spiral branch are inherited from the
base WOA without modification.

Worst-Individual-Disturbance WOA disturbs the classical encircling step with information about the
worst individual in the population, following the individual-disturbance strategy from Qiao et al.
(2022). The encircling update `X_new = X_best - A*D` is replaced with
`X_new = r_4 * X_best - A*D + (1 - r_4) * X_worst`, where `r_4` is drawn uniformly from `[0, 1]`
.This introduces information about the worst individual into the encircling update while retaining the best individual as a reference point.
The exploration branch and the spiral branch stay identical to the base WOA.

Exponential WOA replaces the standard linear schedule of the convergence coefficient a
with a nonlinear schedule based on an exponential function. 
The remaining WOA movement mechanisms are unchanged.

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
    ExponentialDecayWOA,
    ExponentialDecayWOAData,
    FunctionLoader,
    GaussianWOA,
    GaussianWOAData,
    LevyWalkWOA,
    LevyWalkWOAData,
    ModifiedSpiralWOA,
    ModifiedSpiralWOAData,
    MutationWOA,
    MutationWOAData,
    OppositionBasedWOA,
    OppositionWOAData,
    OptimizationType,
    SingleDimensionalWOA,
    SingleDimensionalWOAData,
    WOA,
    WOAData,
    WorstIndividualDisturbanceWOA,
    WorstIndividualDisturbanceWOAData,
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
- most variants spend one evaluation per whale per iteration, but GM-WOA and Opposition-Based WOA
  spend more, so they use up `max_nfe` faster — see their notes below

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

Gaussian WOA usage:

```python
from whalepy import FunctionLoader, GaussianWOA, GaussianWOAData

loader = FunctionLoader()
config = GaussianWOAData(
    population_size=30,
    max_iter=120,
    max_nfe=3800,
    dimension=5,
    lb=[-5.0] * 5,
    ub=[5.0] * 5,
    function=loader.load_callable("ackley"),
    seed=7,
)

result = GaussianWOA(config).run()
print(result.best_fitness_value)
```

Gaussian Mutation WOA (GM-WOA) notes:

- runs the standard WOA update on the whole population, producing positions `X^A`
- then applies a multiplicative Gaussian mutation `X' = X^A * (1 + G)` (element-wise, `G ~ N(0, I)`)
  to every whale, following Luo et al. (2019)
- the mutated candidate is accepted only if it improves the fitness (greedy selection); otherwise the
  standard WOA position `X^A` is kept
- the perturbation scale on coordinate `i` is proportional to `|X^A_i|`, so points near the origin are
  perturbed only slightly and points far from it can move substantially
- the base WOA operators (encircling, spiral update, random exploration) are unchanged; there are no
  additional parameters beyond those inherited from `WOAData`
- one iteration costs two evaluations per whale (the WOA step plus the mutated candidate), so with the
  settings above the run completes 62 full iterations and may enter a partial 63rd one before
  reaching `max_nfe=3800`
- to allow the same number of full iterations as the other variants, GM-WOA requires approximately
  twice the evaluation budget, since each iteration evaluates both the standard WOA candidate and the
  Gaussian-mutated candidate

Opposition-Based WOA usage:

```python
from whalepy import FunctionLoader, OppositionBasedWOA, OppositionWOAData

loader = FunctionLoader()
config = OppositionWOAData(
    population_size=30,
    max_iter=120,
    max_nfe=3800,
    dimension=5,
    lb=[-5.0] * 5,
    ub=[5.0] * 5,
    function=loader.load_callable("ackley"),
    seed=7,
    use_obl_initialization=True,
)

result = OppositionBasedWOA(config).run()
print(result.best_fitness_value)
```

Opposition-Based WOA notes:

- `use_obl_initialization=True` (default) generates an opposite candidate `x_opp = lb + ub - x` for every
  random whale and keeps the best N individuals from the combined pool of 2N candidates as the starting
  population
- `use_obl_initialization=False` disables the OBL step and makes the algorithm behave exactly like base WOA
- the main loop is inherited from base WOA without modification
- initialization costs `2 * population_size` evaluations instead of `population_size`, so `max_nfe`
  must be at least that large or the algorithm raises a `ValueError`

Single-Dimensional WOA usage:

```python
from whalepy import FunctionLoader, SingleDimensionalWOA, SingleDimensionalWOAData

loader = FunctionLoader()
config = SingleDimensionalWOAData(
    population_size=30,
    max_iter=120,
    max_nfe=3800,
    dimension=5,
    lb=[-5.0] * 5,
    ub=[5.0] * 5,
    function=loader.load_callable("ackley"),
    seed=7,
)

result = SingleDimensionalWOA(config).run()
print(result.best_fitness_value)
```

Single-Dimensional WOA notes:

- implements only the single-dimensional swimming mechanism from Du et al. (2020, Symmetry 12(11), 1892)
- whenever the base WOA would run its encircling-prey update (`p < 0.5` and `|A| < 1`), a single
  randomly selected coordinate `d` is updated via `X_d(t+1) = X*_d(t) - A * |C * X*_d(t) - X_d(t)|`
- all other coordinates keep their current values
- the exploration branch and the spiral update are identical to the base WOA
- there are no additional configuration parameters beyond those inherited from `WOAData`

Worst-Individual-Disturbance WOA usage:

```python
from whalepy import (
    FunctionLoader,
    WorstIndividualDisturbanceWOA,
    WorstIndividualDisturbanceWOAData,
)

loader = FunctionLoader()
config = WorstIndividualDisturbanceWOAData(
    population_size=30,
    max_iter=120,
    max_nfe=3800,
    dimension=5,
    lb=[-5.0] * 5,
    ub=[5.0] * 5,
    function=loader.load_callable("ackley"),
    seed=7,
)

result = WorstIndividualDisturbanceWOA(config).run()
print(result.best_fitness_value)
```

Worst-Individual-Disturbance WOA notes:

- implements the individual-disturbance strategy from Qiao et al. (2022), eq. 9
- the classical encircling formula `X_new = X_best - A*D` is replaced with
  `X_new = r_4 * X_best - A*D + (1 - r_4) * X_worst`, where `r_4` is drawn uniformly from `[0, 1]`
- only the individual-disturbance component is retained; the neighborhood mutation search proposed
  alongside it in the same paper is not applied
- the exploration branch and the spiral update are identical to the base WOA
- there are no additional configuration parameters beyond those inherited from `WOAData`

Exponential Decay WOA usage:

```python
from whalepy import ExponentialDecayWOA, ExponentialDecayWOAData, FunctionLoader

loader = FunctionLoader()
config = ExponentialDecayWOAData(
    population_size=30,
    max_iter=120,
    max_nfe=3800,
    dimension=5,
    lb=[-5.0] * 5,
    ub=[5.0] * 5,
    function=loader.load_callable("ackley"),
    seed=7,
    a_initial=2.0,
    a_final=0.0,
    k=0.5,
)

result = ExponentialDecayWOA(config).run()
print(result.best_fitness_value)
```

Exponential Decay WOA notes:

- implements the nonlinear convergence coefficient from Sun et al. (2022, eq. 12):
  `a(t) = a_initial - (a_initial - a_final) * (exp(tau^k) - 1) / (e - 1)`
- if `T` denotes the total number of scheduled iterations, then `tau = t / (T - 1)` for
  `t = 0, ..., T - 1`
- boundary conditions are exact: `a(0) == a_initial` and `a(T - 1) == a_final`
- `k > 0` shapes the curve: smaller values make `a` drop quickly early in the run, larger values keep
  it high for longer (at the halfway point, `k=0.3` gives `a ≈ 0.54` while `k=0.9` gives `a ≈ 1.18`)
- the useful range is problem-dependent, so `k` is exposed as a configuration parameter
- the example above uses `k=0.5` for demonstration; the benchmark experiments run for this project
  used `k=0.7`
- only the update rule for `a` is taken from Sun et al.; the rest of the algorithm
  (encircling, spiral update, random exploration) is identical to the base WOA

Optional convenience helper:

```python
from whalepy import WOA, WOAData, run_algorithm

result = run_algorithm(WOA, WOAData(...))
```

## Benchmarking

The repository includes a simple benchmark runner for comparing all implemented variants on the same benchmark
setup.

Run the full benchmark suite:

```bash
python benchmarks/benchmark_runner.py
```

Run a smaller smoke benchmark:

```bash
python benchmarks/benchmark_runner.py --smoke
```

Write per-run results to CSV:

```bash
python benchmarks/benchmark_runner.py --csv benchmarks/results/benchmark_results.csv
```

The benchmark runner compares:

- WOA
- AdaptiveWOA
- CWOA
- MutationWOA
- ModifiedSpiralWOA
- LevyWalkWOA
- GaussianWOA
- OppositionBasedWOA
- SingleDimensionalWOA
- WorstIndividualDisturbanceWOA
- ExponentialDecayWOA

The default registry includes these benchmark functions:

- Ackley
- Schwefel
- Griewank
- Michalewicz
- Rastrigin
- Rana
- EggHolder
- Rosenbrock

Reported metrics include:

- algorithm name
- function name
- dimension
- run count
- best fitness across runs
- mean best fitness across runs
- standard deviation of best fitness
- average runtime
- average completed epochs
- average function evaluations

## Project Layout

```text
benchmarks/
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
- Gaussian Mutation WOA (GM-WOA) that appends a multiplicative Gaussian perturbation
  `X^A * (1 + G)` with greedy selection after each standard WOA update
- opposition-based WOA that seeds the population with the best N individuals from N random whales and their
  opposite counterparts
- single-dimensional WOA that replaces the encircling-prey step with a single-coordinate update from
  Du et al. (2020)
- worst-individual-disturbance WOA that perturbs the encircling step with information from the worst
  individual, following Qiao et al. (2022)
- exponential decay WOA with an exponential decay schedule for the convergence coefficient
- built-in Ackley, Schwefel, Griewank, Michalewicz, Rastrigin, Rana, EggHolder, and Rosenbrock benchmark callables, with
  Sphere still available for compatibility
- WOA-specific `Whale` and `Population` models
