Getting Started
===============

Every algorithm is used in the same way: create a configuration object for the selected variant,
pass it to the algorithm class, and call ``run()``.

.. code-block:: python

   from whalepy import FunctionLoader, WOA, WOAData

   config = WOAData(
       population_size=30,
       max_iter=100,
       dimension=5,
       lb=[-5.0] * 5,
       ub=[5.0] * 5,
       function=FunctionLoader().load_callable("rastrigin"),
       seed=7,
   )
   result = WOA(config).run()
   print(result.best_fitness_value, result.best_whale.position)

Any Python function that takes a list of decision variables and returns a number can be used
as the objective function. To use another variant, replace ``WOA`` and ``WOAData`` with the
corresponding classes, for example ``CWOA`` and ``CWOAData``.

More examples are available in the ``examples`` directory of the repository.
