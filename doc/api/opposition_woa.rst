OppositionBasedWOA
==================

Improves the initial population with opposition-based learning. For each random whale ``x``, the opposite whale ``lb + ub - x`` is evaluated, and the best ``population_size`` whales of both populations form the initial population. The main loop is the same as in WOA.

.. autoclass:: whalepy.OppositionBasedWOA

.. autoclass:: whalepy.OppositionWOAData

Example
-------

.. literalinclude:: ../../examples/example_09_opposition_woa.py
   :language: python
   :start-at: from whalepy import
