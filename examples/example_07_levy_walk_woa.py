import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from whalepy import LevyWalkWOA
from whalepy.WOAAlgs.data import LevyWalkWOAData
from whalepy.functions.function_loader import FunctionLoader


def main() -> None:
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
    algorithm = LevyWalkWOA(config)
    result = algorithm.run()

    print(f"Algorithm: {algorithm.__class__.__name__}")
    print(f"Epochs completed: {result.epochs_completed}")
    print(f"Function evaluations: {result.nfe}")
    print(f"Best fitness: {result.best_fitness_value}")
    if result.best_whale is not None:
        print(f"Best position: {result.best_whale.position}")


if __name__ == "__main__":
    main()
