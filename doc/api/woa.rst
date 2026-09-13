WOA
===

The original whale optimization algorithm proposed by Mirjalili and Lewis (2016). Each whale encircles the best solution found so far, explores the search space with respect to a randomly selected whale, or performs the spiral bubble-net attack. See :doc:`../woa` for a description of the algorithm.

.. autoclass:: whalepy.WOA

.. autoclass:: whalepy.WOAData

Example
-------

.. literalinclude:: ../../examples/example_01_basic_woa.py
   :language: python
   :start-at: from whalepy import
