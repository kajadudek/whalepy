from whalepy import AdaptiveWOA
from whalepy.WOAAlgs.data import AdaptiveWOAData


def custom_objective(candidate):
    return sum(abs(value) for value in candidate)


def main() -> None:
    config = AdaptiveWOAData(
        population_size=15,
        max_nfe=300,
        dimension=3,
        lb=[-1.0, -1.0, -1.0],
        ub=[1.0, 1.0, 1.0],
        function=custom_objective,
        adaptation_rule="todo",
    )
    algorithm = AdaptiveWOA(config)

    print("This is a scaffold example only.")
    print(f"Prepared algorithm: {algorithm.__class__.__name__}")
    print("The WOA model is centered on whale positions and fitness values.")
    print("TODO: add a runnable optimization example once implementation exists.")


if __name__ == "__main__":
    main()
