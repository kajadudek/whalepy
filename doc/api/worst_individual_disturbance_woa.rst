WorstIndividualDisturbanceWOA
=============================

Replaces the encircling move with the individual disturbance formula ``X_new = r4 * X* - A * |C * X* - X_i| + (1 - r4) * X_worst``, which also uses the position of the worst whale in the population. The exploration and spiral moves are unchanged.

.. autoclass:: whalepy.WorstIndividualDisturbanceWOA

.. autoclass:: whalepy.WorstIndividualDisturbanceWOAData

Example
-------

.. literalinclude:: ../../examples/example_11_worst_individual_disturbance_woa.py
   :language: python
   :start-at: from whalepy import
