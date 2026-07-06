import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from whalepy import FunctionLoader, WOA, WOAData


def main() -> None:
    loader = FunctionLoader()
    config = WOAData(
        population_size=55,
        max_iter=500,
        max_nfe=2200,
        dimension=5,
        lb=[-2.0] * 5,
        ub=[2.0] * 5,
        function=loader.load_callable("rosenbrock"),
        seed=7,
    )
    algorithm = WOA(config)
    result = algorithm.run()

    print(f"Algorithm: {algorithm.__class__.__name__}")
    print(f"Epochs completed: {result.epochs_completed}")
    print(f"Function evaluations: {result.nfe}")
    print(f"Best fitness: {result.best_fitness_value}")
    if result.best_whale is not None:
        print(f"Best position: {result.best_whale.position}")


if __name__ == "__main__":
    main()
