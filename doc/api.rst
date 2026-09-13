API overview
============

Main public modules (the classes are documented in detail on the following pages):

- ``whalepy.WOAAlgs`` -- algorithm classes. All variants inherit from ``BaseWOAAlg``, which
  implements the common optimization loop; ``WOAAlgs.data`` contains the configuration classes
  (``BaseData``, ``WOAData`` and the classes of individual variants), and ``WOAAlgs.methods``
  contains the position update rules.
- ``whalepy.models`` -- ``Whale``, ``Population``, ``AlgorithmResult``, fitness function wrappers,
  ``BoundaryConstraint``, ``OptimizationType`` and stopping conditions
  (``StopCondition``, ``LambdaStopCondition``, ``NeverStopCondition``).
- ``whalepy.functions`` -- built-in benchmark functions available through ``FunctionLoader``.
- ``whalepy.helpers`` -- ``get_logger`` and ``MetricHelper`` for summarizing results.

Parameters shared by all variants (``BaseData``):

- ``function`` -- objective function (required),
- ``dimension`` -- number of decision variables (default 10),
- ``lb``, ``ub`` -- lower and upper bounds (required; a single value is used for all dimensions),
- ``population_size`` -- number of whales (default 30),
- ``max_iter`` -- maximum number of iterations (default 100),
- ``max_nfe`` -- maximum number of objective function evaluations (default not set),
- ``optimization_type`` -- minimization or maximization (default minimization),
- ``boundary_constraints_fun`` -- ``CLIP`` (default), ``REFLECT``, ``RANDOM_RESET``, ``NONE``
  or a user-defined function,
- ``stop_condition`` -- optional user-defined stopping condition,
- ``seed`` -- seed of the random number generator.

``run()`` returns an ``AlgorithmResult`` with the fields ``best_whale``, ``worst_whale``,
``best_fitness_value``, ``worst_fitness_value``, ``mean_fitness_value``, ``std_fitness_value``,
``history``, ``epochs_completed`` and ``nfe``. ``best_whale`` and ``best_fitness_value`` describe
the best solution found during the whole run, and ``history`` contains the best fitness value found
so far after the initialization and after each iteration. ``worst_whale``, ``worst_fitness_value``,
``mean_fitness_value`` and ``std_fitness_value`` describe the final population.
