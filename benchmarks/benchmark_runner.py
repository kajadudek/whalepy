import argparse
import csv
import statistics
import sys
import time
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from whalepy import (
    AdaptiveWOA,
    AdaptiveWOAData,
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
    SingleDimensionalWOA,
    SingleDimensionalWOAData,
    WOA,
    WOAData,
    WorstIndividualDisturbanceWOA,
    WorstIndividualDisturbanceWOAData,
)


@dataclass
class BenchmarkFunctionSpec:
    name: str
    lower_bound: float
    upper_bound: float


@dataclass
class AlgorithmSpec:
    name: str
    algorithm_cls: type
    config_cls: type
    variant_kwargs: dict


@dataclass
class BenchmarkRunResult:
    algorithm_name: str
    function_name: str
    dimension: int
    seed: int
    best_fitness: float
    runtime_seconds: float
    epochs_completed: int
    nfe: int


FUNCTION_SPECS = [
    BenchmarkFunctionSpec(name="ackley", lower_bound=-5.0, upper_bound=5.0),
    BenchmarkFunctionSpec(name="schwefel", lower_bound=-500.0, upper_bound=500.0),
    BenchmarkFunctionSpec(name="griewank", lower_bound=-600.0, upper_bound=600.0),
    BenchmarkFunctionSpec(name="michalewicz", lower_bound=0.0, upper_bound=3.141592653589793),
    BenchmarkFunctionSpec(name="rastrigin", lower_bound=-5.12, upper_bound=5.12),
    BenchmarkFunctionSpec(name="rana", lower_bound=-500.0, upper_bound=500.0),
    BenchmarkFunctionSpec(name="eggholder", lower_bound=-512.0, upper_bound=512.0),
    BenchmarkFunctionSpec(name="rosenbrock", lower_bound=-2.0, upper_bound=2.0),
]

ALGORITHM_SPECS = [
    AlgorithmSpec(name="WOA", algorithm_cls=WOA, config_cls=WOAData, variant_kwargs={}),
    AlgorithmSpec(
        name="AdaptiveWOA",
        algorithm_cls=AdaptiveWOA,
        config_cls=AdaptiveWOAData,
        variant_kwargs={
            "a_strategy": "cosine",
            "use_inertia_weight": True,
            "adaptive_probability": True,
            "p_start": 0.5,
            "p_end": 0.9,
        },
    ),
    AlgorithmSpec(
        name="CWOA",
        algorithm_cls=CWOA,
        config_cls=CWOAData,
        variant_kwargs={
            "chaotic_map": "logistic",
            "chaotic_seed": 0.37,
            "use_chaotic_initialization": True,
            "use_chaotic_probability": True,
            "use_chaotic_coefficients": True,
            "use_chaotic_spiral": True,
            "use_chaotic_a": False,
        },
    ),
    AlgorithmSpec(
        name="MutationWOA",
        algorithm_cls=MutationWOA,
        config_cls=MutationWOAData,
        variant_kwargs={
            "mutation_strategy": "de_rand_1",
            "mutation_factor": 0.6,
            "mutation_probability": 0.35,
            "use_mutation_selection": True,
        },
    ),
    AlgorithmSpec(
        name="ModifiedSpiralWOA",
        algorithm_cls=ModifiedSpiralWOA,
        config_cls=ModifiedSpiralWOAData,
        variant_kwargs={
            "spiral_mode": "archimedean",
            "spiral_b": 1.0,
            "spiral_step": 0.25,
            "spiral_shrink_factor": 0.75,
        },
    ),
    AlgorithmSpec(
        name="LevyWalkWOA",
        algorithm_cls=LevyWalkWOA,
        config_cls=LevyWalkWOAData,
        variant_kwargs={
            "levy_beta": 1.5,
            "levy_scale": 0.05,
            "use_levy_exploration": True,
            "levy_mode": "exploration_only",
        },
    ),
    AlgorithmSpec(
        name="GaussianWOA",
        algorithm_cls=GaussianWOA,
        config_cls=GaussianWOAData,
        variant_kwargs={},
    ),
    AlgorithmSpec(
        name="OppositionBasedWOA",
        algorithm_cls=OppositionBasedWOA,
        config_cls=OppositionWOAData,
        variant_kwargs={
            "use_obl_initialization": True,
        },
    ),
    AlgorithmSpec(
        name="SingleDimensionalWOA",
        algorithm_cls=SingleDimensionalWOA,
        config_cls=SingleDimensionalWOAData,
        variant_kwargs={},
    ),
    AlgorithmSpec(
        name="WorstIndividualDisturbanceWOA",
        algorithm_cls=WorstIndividualDisturbanceWOA,
        config_cls=WorstIndividualDisturbanceWOAData,
        variant_kwargs={},
    ),
    AlgorithmSpec(
        name="ExponentialDecayWOA",
        algorithm_cls=ExponentialDecayWOA,
        config_cls=ExponentialDecayWOAData,
        variant_kwargs={
            "a_initial": 2.0,
            "a_final": 0.0,
            "k": 0.5,
        },
    ),
]


def build_config(
        algorithm_spec: AlgorithmSpec,
        function_spec: BenchmarkFunctionSpec,
        function_loader: FunctionLoader,
        dimension: int,
        population_size: int,
        max_iter: int,
        max_nfe: int | None,
        seed: int,
):
    shared_kwargs = {
        "population_size": population_size,
        "max_iter": max_iter,
        "max_nfe": max_nfe,
        "dimension": dimension,
        "lb": [function_spec.lower_bound] * dimension,
        "ub": [function_spec.upper_bound] * dimension,
        "function": function_loader.load_callable(function_spec.name),
        "seed": seed,
    }
    shared_kwargs.update(algorithm_spec.variant_kwargs)
    return algorithm_spec.config_cls(**shared_kwargs)


def run_single_benchmark(
        algorithm_spec: AlgorithmSpec,
        function_spec: BenchmarkFunctionSpec,
        function_loader: FunctionLoader,
        dimension: int,
        population_size: int,
        max_iter: int,
        max_nfe: int | None,
        seed: int,
) -> BenchmarkRunResult:
    config = build_config(
        algorithm_spec=algorithm_spec,
        function_spec=function_spec,
        function_loader=function_loader,
        dimension=dimension,
        population_size=population_size,
        max_iter=max_iter,
        max_nfe=max_nfe,
        seed=seed,
    )
    algorithm = algorithm_spec.algorithm_cls(config)
    started_at = time.perf_counter()
    result = algorithm.run()
    runtime_seconds = time.perf_counter() - started_at
    return BenchmarkRunResult(
        algorithm_name=algorithm_spec.name,
        function_name=function_spec.name,
        dimension=dimension,
        seed=seed,
        best_fitness=float(result.best_fitness_value),
        runtime_seconds=runtime_seconds,
        epochs_completed=result.epochs_completed,
        nfe=result.nfe,
    )


def summarize_group(run_results: list[BenchmarkRunResult]) -> dict:
    best_values = [run.best_fitness for run in run_results]
    runtimes = [run.runtime_seconds for run in run_results]
    epochs = [run.epochs_completed for run in run_results]
    nfe_values = [run.nfe for run in run_results]
    return {
        "algorithm": run_results[0].algorithm_name,
        "function": run_results[0].function_name,
        "dimension": run_results[0].dimension,
        "runs": len(run_results),
        "best_fitness": min(best_values),
        "mean_fitness": statistics.mean(best_values),
        "std_fitness": 0.0 if len(best_values) == 1 else statistics.stdev(best_values),
        "avg_runtime": statistics.mean(runtimes),
        "avg_epochs": statistics.mean(epochs),
        "avg_nfe": statistics.mean(nfe_values),
    }


def format_summary_table(summary_rows: list[dict]) -> str:
    headers = [
        "algorithm",
        "function",
        "dim",
        "runs",
        "best",
        "mean",
        "std",
        "avg_time_s",
        "avg_epochs",
        "avg_nfe",
    ]
    table_rows = []
    for row in summary_rows:
        table_rows.append(
            [
                row["algorithm"],
                row["function"],
                str(row["dimension"]),
                str(row["runs"]),
                f"{row['best_fitness']:.6e}",
                f"{row['mean_fitness']:.6e}",
                f"{row['std_fitness']:.6e}",
                f"{row['avg_runtime']:.4f}",
                f"{row['avg_epochs']:.2f}",
                f"{row['avg_nfe']:.2f}",
            ]
        )
    widths = [len(header) for header in headers]
    for row in table_rows:
        for index, value in enumerate(row):
            widths[index] = max(widths[index], len(value))

    def format_row(values: list[str]) -> str:
        return " | ".join(value.ljust(widths[index]) for index, value in enumerate(values))

    separator = "-+-".join("-" * width for width in widths)
    lines = [format_row(headers), separator]
    lines.extend(format_row(row) for row in table_rows)
    return "\n".join(lines)


def write_csv_results(output_path: Path, run_results: list[BenchmarkRunResult]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="ascii", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "algorithm_name",
                "function_name",
                "dimension",
                "seed",
                "best_fitness",
                "runtime_seconds",
                "epochs_completed",
                "nfe",
            ],
        )
        writer.writeheader()
        for run in run_results:
            writer.writerow(
                {
                    "algorithm_name": run.algorithm_name,
                    "function_name": run.function_name,
                    "dimension": run.dimension,
                    "seed": run.seed,
                    "best_fitness": run.best_fitness,
                    "runtime_seconds": run.runtime_seconds,
                    "epochs_completed": run.epochs_completed,
                    "nfe": run.nfe,
                }
            )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run benchmark comparisons for whalepy variants.")
    parser.add_argument("--dimension", type=int, default=10)
    parser.add_argument("--population-size", type=int, default=30)
    parser.add_argument("--max-iter", type=int, default=120)
    parser.add_argument("--max-nfe", type=int, default=5000)
    parser.add_argument("--runs", type=int, default=3)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--csv", type=Path, default=None)
    parser.add_argument(
        "--smoke",
        action="store_true",
        help="Run a smaller smoke benchmark for quick validation.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    dimension = args.dimension
    population_size = args.population_size
    max_iter = args.max_iter
    max_nfe = args.max_nfe
    runs = args.runs

    if args.smoke:
        dimension = 5
        population_size = 15
        max_iter = 20
        max_nfe = 500
        runs = 1

    function_loader = FunctionLoader()
    run_results: list[BenchmarkRunResult] = []

    for function_spec in FUNCTION_SPECS:
        for algorithm_spec in ALGORITHM_SPECS:
            for run_index in range(runs):
                seed = args.seed + run_index
                run_results.append(
                    run_single_benchmark(
                        algorithm_spec=algorithm_spec,
                        function_spec=function_spec,
                        function_loader=function_loader,
                        dimension=dimension,
                        population_size=population_size,
                        max_iter=max_iter,
                        max_nfe=max_nfe,
                        seed=seed,
                    )
                )

    summary_rows = []
    for function_spec in FUNCTION_SPECS:
        for algorithm_spec in ALGORITHM_SPECS:
            group = [
                run
                for run in run_results
                if run.function_name == function_spec.name and run.algorithm_name == algorithm_spec.name
            ]
            summary_rows.append(summarize_group(group))

    print("whalepy benchmark summary")
    print(
        f"dimension={dimension}, population_size={population_size}, max_iter={max_iter}, "
        f"max_nfe={max_nfe}, runs={runs}, seed_base={args.seed}"
    )
    print()
    print(format_summary_table(summary_rows))

    if args.csv is not None:
        write_csv_results(args.csv, run_results)
        print()
        print(f"CSV results written to: {args.csv}")


if __name__ == "__main__":
    main()
