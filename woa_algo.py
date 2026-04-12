import numpy as py

py.random.seed(42)

class WOA:
    def __init__(self, f, upper_bound, lower_bound, whale_num, iters, spiral_const=1):
        self.f = f
        self.upper_bound = upper_bound
        self.lower_bound = lower_bound
        self.whale_num = whale_num
        self.iters = iters
        self.whales = {}
        self.prey = {}
        self.spiral_const = spiral_const

    def init_whales(self):
        self.whales['pos'] = py.array(
            [py.random.uniform(self.lower_bound, self.upper_bound, size=(len(self.lower_bound),)) for _ in
             range(self.whale_num)])
        self.whales['fit'] = self.f(self.whales['pos'])

    def init_prey(self):
        best_idx = self.whales['fit'].argmin()
        self.prey['pos'] = self.whales['pos'][[best_idx]]
        self.prey['fit'] = self.whales['fit'][[best_idx]]

    def encircle(self, i, A, C):
        d = py.abs(C[..., py.newaxis] * self.prey['pos'] - self.whales['pos'][i])
        self.whales['pos'][i] = py.clip(self.prey['pos'][0] - A[..., py.newaxis] * d, self.lower_bound,
                                        self.upper_bound)

    def search(self, i, A, C):
        rand_whale = self.whales['pos'][py.random.randint(low=0, high=self.whale_num, size=len(i[0]))]
        d = py.abs(C[..., py.newaxis] * rand_whale - self.whales['pos'][i])
        self.whales['pos'][i] = py.clip(rand_whale - A[..., py.newaxis] * d, self.lower_bound, self.upper_bound)

    def bubble_net_fishing(self, i):
        d = py.abs(self.prey['pos'] - self.whales['pos'][i])
        l = py.random.uniform(-1, 1, size=len(i[0]))
        self.whales['pos'][i] = py.clip(
            py.cos(2 * py.pi * l)[..., py.newaxis] * py.exp(self.spiral_const * l)[..., py.newaxis] * d + self.prey[
                'pos'],
            self.lower_bound, self.upper_bound
        )

    def optimize(self, a):
        r1 = py.random.random(self.whale_num)
        r2 = py.random.random(self.whale_num)
        A = 2 * a * r1 - a
        C = 2 * r2

        p = py.random.random(self.whale_num)

        encircle_idx = py.where((p < 0.5) & (py.abs(A) <= 1))
        search_idx = py.where((p < 0.5) & (py.abs(A) > 1))
        bubble_idx = py.where(p >= 0.5)

        self.encircle(encircle_idx, A[encircle_idx], C[encircle_idx])
        self.search(search_idx, A[search_idx], C[search_idx])
        self.bubble_net_fishing(bubble_idx)

        self.whales['fit'] = self.f(self.whales['pos'])

    def update_prey(self):
        if self.prey['fit'][0] > self.whales['fit'].min():
            self.prey['pos'][0] = self.whales['pos'][self.whales['fit'].argmin()]
            self.prey['fit'][0] = self.whales['fit'].min()

    def run(self):
        self.init_whales()
        self.init_prey()
        results = [self.prey['fit'][0]]

        for i in range(self.iters):
            a = 2 - i * (2 / self.iters)

            self.optimize(a)
            self.update_prey()

            results.append(self.prey['fit'][0])

        result_x = self.prey['pos'].squeeze()

        return results, result_x


# ===================== TEST =======================

def f(x):
    return py.sum(x ** 2, axis=1)


# sphere
def f2(x):
    return py.sum(x ** 2, axis=1)


# rosenbrock
def f3(x):
    return py.sum(100 * (x[:, 1:] - x[:, :-1] ** 2) ** 2 + (1 - x[:, :-1]) ** 2, axis=1)


functions = [
    ("Sphere", f),
    ("Sphere (duplicate)", f2),
    ("Rosenbrock", f3),
]

for name, func in functions:
    print(f"\n=== {name} ===")

    woa = WOA(func, [10, 10], [-10, -10], 10, 20)  # 2D for Rosenbrock
    results, best = woa.run()

    print("Results:")
    print("  values:", [float(v) for v in results])
    print("  best x:", best)
    print("  best y:", float(results[-1]))
