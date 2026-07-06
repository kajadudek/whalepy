import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from whalepy import WOA, WOAData


def custom_objective(candidate):
    return sum(abs(value) + 0.1 * value * value for value in candidate)


def main() -> None:
    config = WOAData(
        population_size=20,
        max_iter=60,
        max_nfe=1500,
        dimension=3,
        lb=[-4.0, -4.0, -4.0],
        ub=[4.0, 4.0, 4.0],
        function=custom_objective,
        seed=11,
    )
    algorithm = WOA(config)
    result = algorithm.run()

    print(f"Algorithm: {algorithm.__class__.__name__}")
    print(f"Best fitness: {result.best_fitness_value}")
    if result.best_whale is not None:
        print(f"Best position: {result.best_whale.position}")


if __name__ == "__main__":
    main()
