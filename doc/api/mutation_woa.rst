MutationWOA
===========

After the standard WOA update, a mutation candidate is created with a given probability using the DE/rand/1 strategy from differential evolution. By default, the better of the WOA candidate and the mutation candidate is kept.

.. autoclass:: whalepy.MutationWOA

.. autoclass:: whalepy.MutationWOAData

Example
-------

.. literalinclude:: ../../examples/example_05_mutation_woa.py
   :language: python
   :start-at: from whalepy import
