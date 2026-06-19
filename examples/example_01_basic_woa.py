from whalepy import WOA
from whalepy.WOAAlgs.data import WOAData


def sphere(candidate):
    return sum(value * value for value in candidate)


def main() -> None:
    config = WOAData(
        population_size=20,
        max_nfe=500,
        dimension=5,
        lb=[-10.0] * 5,
        ub=[10.0] * 5,
        function=sphere,
    )
    algorithm = WOA(config)

    print("This is a scaffold example only.")
    print(f"Prepared algorithm: {algorithm.__class__.__name__}")
    print("The WOA model is centered on whale positions and fitness values.")
    print("TODO: enable algorithm.run() after the optimizer is implemented.")


if __name__ == "__main__":
    main()
