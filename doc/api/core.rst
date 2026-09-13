Core classes
============

Base algorithm
--------------

All variants inherit from :class:`~whalepy.WOAAlgs.base.BaseWOAAlg`, which implements the
common optimization loop.

.. autoclass:: whalepy.WOAAlgs.base.BaseWOAAlg
   :members: run, next_epoch, initialization_nfe_cost, epoch_nfe_cost

Configuration
-------------

.. autoclass:: whalepy.BaseData

Result
------

.. autoclass:: whalepy.AlgorithmResult

.. autoclass:: whalepy.Whale

Optimization type and boundary handling
---------------------------------------

.. autoclass:: whalepy.OptimizationType
   :members:
   :undoc-members:

.. autoclass:: whalepy.BoundaryConstraint
   :members:
   :undoc-members:

Stopping conditions
-------------------

.. autoclass:: whalepy.models.stop_condition.StopCondition
   :members: should_stop

.. autoclass:: whalepy.models.stop_condition.LambdaStopCondition

.. autoclass:: whalepy.models.stop_condition.NeverStopCondition

Benchmark functions
-------------------

.. autoclass:: whalepy.FunctionLoader
   :members: list_functions, load_callable, load_metadata

Helpers
-------

.. autoclass:: whalepy.helpers.MetricHelper
   :members:
