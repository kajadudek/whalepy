AdaptiveWOA
===========

Replaces the linear decrease of the coefficient ``a`` with a nonlinear (cosine or logarithmic) schedule, adds an adaptive inertia weight in the encircling move, and increases the probability of the spiral move during the run.

.. autoclass:: whalepy.AdaptiveWOA

.. autoclass:: whalepy.AdaptiveWOAData

Example
-------

.. literalinclude:: ../../examples/example_03_adaptive_woa.py
   :language: python
   :start-at: from whalepy import
