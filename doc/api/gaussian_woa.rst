GaussianWOA
===========

After the standard WOA update, applies a multiplicative Gaussian mutation ``X' = X * (1 + G)``, where ``G ~ N(0, I)``, to every whale. The mutated position is accepted only if it improves the fitness value.

.. autoclass:: whalepy.GaussianWOA

.. autoclass:: whalepy.GaussianWOAData

Example
-------

.. literalinclude:: ../../examples/example_08_gaussian_woa.py
   :language: python
   :start-at: from whalepy import
