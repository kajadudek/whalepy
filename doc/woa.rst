WOA
===

The original Whale Optimization Algorithm (Mirjalili and Lewis, 2016) is implemented in
``whalepy.WOAAlgs.woa`` (class ``WOA``, configuration class ``WOAData``).

The algorithm maintains a population of whales, each representing a candidate solution.
In every iteration, each whale draws the coefficients ``A = 2 * a * r1 - a`` and ``C = 2 * r2``,
where ``a`` decreases linearly from 2 to 0, and a random number ``p``:

- if ``p < 0.5`` and ``|A| < 1``, the whale encircles the best solution found so far (the leader),
- if ``p < 0.5`` and ``|A| >= 1``, the whale moves with respect to a randomly selected whale
  (exploration),
- if ``p >= 0.5``, the whale performs the logarithmic spiral move around the leader
  (``spiral_constant`` defines the shape of the spiral, default 1.0).

After the update, positions outside the search space are repaired with the selected boundary
handling strategy and the whales are evaluated. The leader is replaced only when a better
solution has been found, so it is always the best solution found so far, while the worst whale
is taken from the current population.
The run stops when ``max_iter`` or ``max_nfe`` is reached or when the user-defined stopping
condition is met. The update rules are implemented in ``whalepy.WOAAlgs.methods.methods_woa``.
