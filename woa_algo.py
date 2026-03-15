import numpy as py

class WOA:
    def __init__(self, f, upper_bound, lower_bound, whale_num, iters):
        self.f = f
        self.upper_bound = upper_bound
        self.lower_bound = lower_bound
        self.whale_num = whale_num
        self.iters = iters
        self.whales = {}
        self.prey = {}

    def init_whales(self):
        self.whales['pos'] = py.random.uniform(self.lower_bound, self.upper_bound, self.whale_num)
        print(self.whales['pos'])
        self.whales['fit'] = self.f(self.whales['pos'])
        print(self.whales['fit'])

    def init_prey(self):
        self.prey['pos'] = py.random.uniform(self.lower_bound, self.upper_bound, self.whale_num)
        self.prey['fit'] = self.f(self.prey['pos'])

    def run(self):
        self.init_whales()
        self.init_prey()

        for i in range(self.iters):
            print(f'Iteration {i}')

        return

woa = WOA(py.sin, 10, -10, 10, 10)
woa.init_whales()