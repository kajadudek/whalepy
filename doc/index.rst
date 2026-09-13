WhalePy
=======

WhalePy is an open-source Python library that provides the original whale optimization
algorithm (WOA) and 10 of its modifications within a common interface. It is intended for
solving continuous single-objective optimization problems and for comparing WOA variants
under the same conditions.

Main features:

- the original WOA and 10 of its variants, each implemented on the basis of its original
  publication,
- a common interface: switching between variants requires only a change of the algorithm
  class and its configuration class,
- any Python function can be used as the objective function; minimization and
  maximization are supported,
- stopping criteria based on the number of iterations, the number of objective function
  evaluations, or a user-defined condition,
- several boundary handling strategies,
- reproducible runs with a random seed,
- nine built-in benchmark functions and a benchmark runner for comparing all variants,
- pure Python with no external dependencies (Python 3.10 or newer).

The source code is available at https://github.com/kajadudek/whalepy.

.. toctree::
   :maxdepth: 2
   :caption: General

   installation
   getting_started
   woa
   variants

.. toctree::
   :maxdepth: 1
   :caption: API

   api
   api/core
   api/woa
   api/adaptive_woa
   api/cwoa
   api/mutation_woa
   api/modified_spiral_woa
   api/levy_walk_woa
   api/gaussian_woa
   api/opposition_woa
   api/single_dimensional_woa
   api/worst_individual_disturbance_woa
   api/exponential_decay_woa

.. toctree::
   :maxdepth: 2
   :caption: Examples

   examples
