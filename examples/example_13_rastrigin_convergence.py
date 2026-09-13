"""Example 13: tracking the optimization process of WOA on the Rastrigin function.

The script runs the original WOA on the two-dimensional Rastrigin function and
records the state of the population after every iteration. The recording is
done with a LambdaStopCondition, which is called by the algorithm after the
initialization and after each iteration, so no changes to the library are
needed. The results are saved as a PDF figure with:
  - the positions of the whales at selected iterations,
  - the best fitness found so far, and the mean and the standard deviation
    of fitness in the population per iteration.

Requires matplotlib (pip install matplotlib).
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import matplotlib.pyplot as plt
import numpy as np

from whalepy import WOA, WOAData, FunctionLoader
from whalepy.models.stop_condition import LambdaStopCondition

plt.rcParams["pdf.fonttype"] = 42  # embed TrueType fonts in the PDF instead of Type 3
# The figure is sized for the text width of a journal page (about 5.4 in), so fonts keep their size.
plt.rcParams.update({"font.size": 8, "axes.titlesize": 8, "axes.labelsize": 8,
                     "xtick.labelsize": 7, "ytick.labelsize": 7, "legend.fontsize": 7})
OUTPUT_DIR = Path(__file__).resolve().parent / "results"
SNAPSHOT_ITERATIONS = (0, 5, 20)


def make_recorder(log: list[dict]):
    def record(algorithm, best_whale) -> bool:
        population = algorithm.population
        log.append(
            {
                "iteration": algorithm.current_epoch,
                "nfe": algorithm.fitness_function.evaluations,
                "positions": [list(whale.position) for whale in population.whales],
                "best": best_whale.fitness_value,
                "mean": population.mean_fitness(),
                "std": population.std_fitness(),
            }
        )
        return False  # never stop early; max_iter controls the run

    return record


def plot_results(log: list[dict], function, lb: float, ub: float, output_path: Path) -> None:
    grid = np.linspace(lb, ub, 400)
    xx, yy = np.meshgrid(grid, grid)
    zz = np.vectorize(lambda x, y: function([x, y]))(xx, yy)

    fig, axes = plt.subplots(2, 3, figsize=(5.4, 4.0))
    by_iteration = {entry["iteration"]: entry for entry in log}

    for axis, iteration in zip(axes[0], SNAPSHOT_ITERATIONS):
        axis.contourf(xx, yy, zz, levels=40, cmap="viridis", zorder=0)
        axis.set_rasterization_zorder(1)  # keeps the PDF small: contours as an image, the rest as vector graphics
        positions = np.array(by_iteration[iteration]["positions"])
        axis.scatter(positions[:, 0], positions[:, 1], c="white", edgecolors="black", s=9, linewidths=0.5, zorder=3)
        axis.plot(0, 0, marker="*", color="red", markersize=7, zorder=2)
        axis.set_title(f"Iteration {iteration}")
        axis.set_xlabel("$x_1$", labelpad=1)
        axis.set_ylabel("$x_2$", labelpad=1)
        axis.set_xlim(lb, ub)
        axis.set_ylim(lb, ub)

    iterations = [entry["iteration"] for entry in log]
    panels = [
        ("best", "Best fitness so far", "Fitness value", "tab:blue"),
        ("mean", "Mean fitness", "Fitness value", "tab:orange"),
        ("std", "Std. dev. of fitness", "Standard deviation", "tab:green"),
    ]
    for axis, (key, title, ylabel, color) in zip(axes[1], panels):
        axis.plot(iterations, [entry[key] for entry in log], color=color, linewidth=1.0)
        axis.set_title(title)
        axis.set_xlabel("Iteration")
        axis.set_ylabel(ylabel)
        axis.grid(alpha=0.3)

    fig.tight_layout(pad=0.4, w_pad=0.6, h_pad=0.8)
    fig.savefig(output_path, dpi=300)
    plt.close(fig)


def main() -> None:
    lb, ub = -5.12, 5.12
    rastrigin = FunctionLoader().load_callable("rastrigin")
    log: list[dict] = []

    config = WOAData(
        population_size=30,
        max_iter=100,
        dimension=2,
        lb=[lb, lb],
        ub=[ub, ub],
        function=rastrigin,
        seed=42,
        stop_condition=LambdaStopCondition(make_recorder(log)),
    )
    result = WOA(config).run()

    print(f"Iterations completed: {result.epochs_completed}")
    print(f"Function evaluations: {result.nfe}")
    print(f"Best fitness: {result.best_fitness_value}")
    print(f"Best position: {result.best_whale.position}")

    OUTPUT_DIR.mkdir(exist_ok=True)
    output_path = OUTPUT_DIR / "example_13_rastrigin_woa.pdf"
    plot_results(log, rastrigin, lb, ub, output_path)
    print(f"Figure saved to: {output_path}")


if __name__ == "__main__":
    main()
