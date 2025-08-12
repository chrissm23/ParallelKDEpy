# API Reference

This section provides an overview of the API of [ParallelKDEpy](https://github.com/chrissm23/ParallelKDE) as well as other tools avaiable in the package. For more detailed information, please refer to the documentation of [ParallelKDE.jl](https://github.com/chrissm23/ParallelKDE.jl).

## Grids

The package exposes the grid objects available in `ParallelKDE.jl` for use in Python. These grids can be used to define the grid on which the kernel density estimation is performed.

```{eval-rst}
.. autoclass:: parallelkdepy.Grid
  :members:
  :inherited-members:
  :show-inheritance:
  :noindex:
  ```

## Estimation
`DensityEstimation` is the main class for performing kernel density estimation in `ParallelKDEpy`. It provides methods for estimating densities on various grids and with different parameters.

The actual density estimation takes place when calling the `estimate_density` method. It takes the name of an estimator as a string, and keyword arguments corresponding to the parameters of the estimator.

```{note}
Available estimators and their parameters are described in the [ParallelKDE.jl documentation].
```

```{eval-rst}
.. autoclass:: parallelkdepy.DensityEstimation
  :members:
  :inherited-members:
  :show-inheritance:
  :noindex:
```

## Dirac sequences

For convenience, the Dirac sequences corresponding to a dataset on a grid can be generated with a `Grid` instance with `initialize_dirac_sequence`.

```{eval-rst}
.. autofunction:: parallelkdepy.initialize_dirac_sequence
  :noindex:
```

## Complete list of modules

```{eval-rst}
.. autosummary::
  :toctree: generated/wrapper
  :recursive:

  parallelkdepy.wrapper
```

```{eval-rst}
.. autosummary::
  :toctree: generated/core
  :recursive:

  parallelkdepy.core
```
