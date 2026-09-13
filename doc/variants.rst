Variants
========

Implemented variants and their reference publications (the parameters of each variant are
described on its API page):

- ``WOA`` -- Mirjalili and Lewis (2016).
- ``AdaptiveWOA`` -- nonlinear (cosine or logarithmic) schedule of ``a``, adaptive inertia weight
  and adaptive spiral probability; Trivedi et al. (2016), Chen et al. (2020), Sun et al. (2022).
- ``CWOA`` -- random numbers replaced with logistic, tent or sine chaotic maps, optional chaotic
  initialization; Kaur and Arora (2018).
- ``MutationWOA`` -- DE/rand/1 mutation applied after the WOA update, accepted if it improves the
  candidate; Mostafa Bozorgi and Yazdani (2019).
- ``ModifiedSpiralWOA`` -- logarithmic or Archimedean-style spiral in the bubble-net attack;
  Sun et al. (2018).
- ``LevyWalkWOA`` -- Levy flights (Mantegna's algorithm) in the exploration phase;
  Ling et al. (2017).
- ``GaussianWOA`` -- multiplicative Gaussian mutation with greedy selection; Luo et al. (2019).
- ``OppositionBasedWOA`` -- opposition-based initialization; Alamri et al. (2018).
- ``SingleDimensionalWOA`` -- single-dimensional encircling update; Du et al. (2020).
- ``WorstIndividualDisturbanceWOA`` -- encircling update disturbed by the worst individual;
  Qiao et al. (2022).
- ``ExponentialDecayWOA`` -- exponential schedule of ``a``; Sun et al. (2022).

Full references are listed in the README and in the docstring of every algorithm class.

Notes on selected variants:

- Gaussian Mutation WOA (GM-WOA): keeps the standard WOA update unchanged and
  appends a multiplicative Gaussian mutation ``X' = X^A * (1 + G)``
  (element-wise, ``G ~ N(0, I)``) applied to every whale after the WOA step,
  where ``X^A`` is the WOA-updated position. The mutated candidate replaces
  ``X^A`` only if it improves the fitness (greedy selection); otherwise ``X^A``
  is kept. Follows Luo et al. (2019).

- Opposition-Based WOA: reuses the base WOA main loop unchanged and modifies only
  the initialization step. A pool of N random whales and their opposite
  counterparts (``x_opp = lb + ub - x``) is evaluated, and the best N individuals
  form the starting population.

- Single-Dimensional WOA: keeps the base WOA loop and replaces only the
  encircling-prey step with the single-dimensional swimming mechanism from
  Du et al. (2020, Symmetry 12(11), 1892, Section 3.4). Whenever the base WOA
  would run its encircling update, a random coordinate ``d`` is selected and
  updated via ``D_d = |C * X*_d(t) - X_d(t)|`` and
  ``X_d(t+1) = X*_d(t) - A * D_d``; all other coordinates keep their current
  values. The exploration branch and the spiral update are unchanged.

- Worst-Individual-Disturbance WOA: keeps the base WOA loop and replaces only
  the encircling-prey step with the individual-disturbance formula from
  Qiao et al. (2022), equation (9):
  ``X_new = r_4 * X_best - A * |C * X_best - X_i| + (1 - r_4) * X_worst``,
  where ``r_4`` is drawn uniformly from ``[0, 1]``. Only the
  individual-disturbance component is retained; the neighborhood mutation
  search proposed alongside it is not applied. The exploration branch and the
  spiral update are unchanged.

- Exponential Decay WOA: replaces the standard linear schedule of the
  convergence coefficient ``a`` with the nonlinear exponential schedule
  proposed by Sun et al. (2022, eq. 12),
  ``a(t) = a_initial - (a_initial - a_final) * (exp(tau^k) - 1) / (e - 1)``,
  with ``tau = t / (T - 1)`` for ``t = 0, ..., T - 1``. Boundary conditions
  are exact (``a(0) = a_initial``, ``a(T - 1) = a_final``); the curve-shape
  parameter ``k > 0`` is configurable. Only the ``a`` update is adopted from
  Sun et al.; the remaining WOA operators are unchanged.
