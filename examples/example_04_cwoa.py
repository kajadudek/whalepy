import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from whalepy import CWOA
from whalepy.WOAAlgs.data import CWOAData
from whalepy.functions.function_loader import FunctionLoader


def main() -> None:
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
        use_chaotic_a=False,
    )
    algorithm = CWOA(config)
    result = algorithm.run()

    print(f"Algorithm: {algorithm.__class__.__name__}")
    print(f"Epochs completed: {result.epochs_completed}")
    print(f"Function evaluations: {result.nfe}")
    print(f"Best fitness: {result.best_fitness_value}")
    if result.best_whale is not None:
        print(f"Best position: {result.best_whale.position}")


if __name__ == "__main__":
    main()
