"""Example 14: comparison of all WOA variants implemented in whalepy.

All variants are run with their default parameters on the same problem
(10-dimensional Schwefel function), with the same population size, the same
budget of objective function evaluations, and the same random seeds. For every
variant, the best fitness value found so far is recorded after each iteration
together with the number of function evaluations used. The script saves:
  - a PDF figure with the mean convergence curves over independent runs,
  - a CSV file with the convergence data of every run.

Since some variants evaluate more candidate solutions per iteration than
others, the curves are plotted against the number of function evaluations.

Requires matplotlib (pip install matplotlib).
"""

import csv
import statistics
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import matplotlib.pyplot as plt

from whalepy import (
    CWOA,
    WOA,
    AdaptiveWOA,
    AdaptiveWOAData,
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
    SingleDimensionalWOA,
    SingleDimensionalWOAData,
    WOAData,
    WorstIndividualDisturbanceWOA,
    WorstIndividualDisturbanceWOAData,
)
from whalepy.models.stop_condition import LambdaStopCondition

plt.rcParams["pdf.fonttype"] = 42  # embed TrueType fonts in the PDF instead of Type 3
# The figure is sized for the text width of a journal page (about 5.4 in), so fonts keep their size.
plt.rcParams.update({"font.size": 8, "axes.titlesize": 8, "axes.labelsize": 8,
                     "xtick.labelsize": 7, "ytick.labelsize": 7, "legend.fontsize": 7})
OUTPUT_DIR = Path(__file__).resolve().parent / "results"

VARIANTS = [
    (WOA, WOAData),
    (AdaptiveWOA, AdaptiveWOAData),
    (CWOA, CWOAData),
    (MutationWOA, MutationWOAData),
    (ModifiedSpiralWOA, ModifiedSpiralWOAData),
    (LevyWalkWOA, LevyWalkWOAData),
    (GaussianWOA, GaussianWOAData),
    (OppositionBasedWOA, OppositionWOAData),
    (SingleDimensionalWOA, SingleDimensionalWOAData),
    (WorstIndividualDisturbanceWOA, WorstIndividualDisturbanceWOAData),
    (ExponentialDecayWOA, ExponentialDecayWOAData),
]

FUNCTION_NAME = "schwefel"
DIMENSION = 10
LOWER_BOUND, UPPER_BOUND = -500.0, 500.0
POPULATION_SIZE = 30
MAX_NFE = 15000
RUNS = 10
NFE_GRID = list(range(POPULATION_SIZE, MAX_NFE + 1, 150))


def run_variant(algorithm_cls, config_cls, function, seed: int) -> list[tuple[int, float]]:
    """Returns (nfe, best fitness found so far) recorded after each iteration."""
    trace: list[tuple[int, float]] = []

    def record(algorithm, best_whale) -> bool:
        # best_whale is the best solution found so far by the algorithm.
        trace.append((algorithm.fitness_function.evaluations, best_whale.fitness_value))
        return False

    config = config_cls(
        population_size=POPULATION_SIZE,
        max_iter=None,
        max_nfe=MAX_NFE,
        dimension=DIMENSION,
        lb=[LOWER_BOUND] * DIMENSION,
        ub=[UPPER_BOUND] * DIMENSION,
        function=function,
        seed=seed,
        stop_condition=LambdaStopCondition(record),
    )
    algorithm_cls(config).run()
    return trace


def value_at(trace: list[tuple[int, float]], nfe: int) -> float:
    """Best fitness found so far after at most `nfe` evaluations."""
    value = trace[0][1]
    for used, best in trace:
        if used > nfe:
            break
        value = best
    return value


def main() -> None:
    function = FunctionLoader().load_callable(FUNCTION_NAME)
    OUTPUT_DIR.mkdir(exist_ok=True)

    mean_curves: dict[str, list[float]] = {}
    final_values: dict[str, list[float]] = {}

    csv_path = OUTPUT_DIR / "example_14_convergence.csv"
    with csv_path.open("w", newline="", encoding="ascii") as handle:
        writer = csv.writer(handle)
        writer.writerow(["algorithm", "run", "seed", "iteration", "nfe", "best_fitness_so_far"])
        for algorithm_cls, config_cls in VARIANTS:
            name = algorithm_cls.__name__
            curves = []
            final_values[name] = []
            for run in range(RUNS):
                seed = run + 1
                trace = run_variant(algorithm_cls, config_cls, function, seed)
                for iteration, (used, best) in enumerate(trace):
                    writer.writerow([name, run + 1, seed, iteration, used, best])
                curves.append([value_at(trace, nfe) for nfe in NFE_GRID])
                final_values[name].append(trace[-1][1])
            mean_curves[name] = [statistics.mean(values) for values in zip(*curves)]
            print(
                f"{name:30s} mean best = {statistics.mean(final_values[name]):10.4f} "
                f"(std {statistics.stdev(final_values[name]):9.4f})"
            )

    fig, axis = plt.subplots(figsize=(5.4, 4.0))
    colors = plt.get_cmap("tab20").colors
    styles = ["-", "--", "-.", ":"]
    for index, (name, curve) in enumerate(mean_curves.items()):
        axis.plot(NFE_GRID, curve, label=name, color=colors[index * 2 % 20 + index // 10],
                  linestyle=styles[index % len(styles)], linewidth=1.2)
    axis.set_yscale("log")
    axis.set_xlabel("Number of function evaluations")
    axis.set_ylabel("Mean best fitness value")
    axis.grid(alpha=0.35, which="major")
    axis.grid(alpha=0.12, which="minor")
    axis.legend(loc="upper center", bbox_to_anchor=(0.5, -0.14), ncol=3, frameon=False,
                handlelength=2.5, columnspacing=1.2)
    fig.tight_layout(pad=0.4)
    figure_path = OUTPUT_DIR / "example_14_variants_comparison.pdf"
    fig.savefig(figure_path)
    plt.close(fig)

    print(f"Convergence data saved to: {csv_path}")
    print(f"Figure saved to: {figure_path}")


if __name__ == "__main__":
    main()
