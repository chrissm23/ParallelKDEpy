Usage Guide
===========

Basic example
-------------

.. code-block:: python

   import numpy as np
   from parallelkdepy import estimate_kde

   data = np.random.randn(1000)
   grid, density = estimate_kde(data, bandwidth=1.0)
   # plot with matplotlib or analyze results...

Advanced options
----------------

- **bandwidth**: smoothing parameter
- **kwargs**: pass through to Julia’s ParallelKDE.kde, e.g. `kernel="gaussian"`.

