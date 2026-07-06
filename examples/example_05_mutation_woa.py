import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from whalepy import FunctionLoader, MutationWOA, MutationWOAData


def main() -> None:
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
    algorithm = MutationWOA(config)
    result = algorithm.run()

    print(f"Algorithm: {algorithm.__class__.__name__}")
    print(f"Epochs completed: {result.epochs_completed}")
    print(f"Function evaluations: {result.nfe}")
    print(f"Best fitness: {result.best_fitness_value}")
    if result.best_whale is not None:
        print(f"Best position: {result.best_whale.position}")


if __name__ == "__main__":
    main()
