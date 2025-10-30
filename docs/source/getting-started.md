# Getting Started

Here, we will exemplify the basic usage of `ParallelKDEpy` with the core estimator `gradepro`. For more details about the existing estimators, their parameters, as well as the more in-depth implementation details, please refer to the [ParallelKDE.jl documentation].

To estimate a density on CPU with a default grid using the `gradepro`, you can use the following code:

```{literalinclude} scripts/plot_kde.py
:language: python
:start-after: [docs-start]
:end-before: [docs-end]
```

```{image} _static/figures/getting-started.png
:alt: Kernel Density Estimate
:align: center
:width: 600
```

That's it! See the {section}`api` for more details on the available methods and parameters.
