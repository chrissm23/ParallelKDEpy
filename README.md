# ParallelKDEpy
Python wrapper of ParallelKDE.jl

## Installation
Since the package is not yet available on PyPI, it is available directly from the GitHub repository:

```bash
git clone https://github.com/chrissm23/ParallelKDEpy.git
```

The local installation is recommended using [poetry](https://python-poetry.org/) which provides installation instructions [here](https://python-poetry.org/docs).

```bash
poetry install
```

> [!WARNING]
> Since `ParallelKDE.jl` is still a private repository, please check the [Advanced installation of `ParallelKDE.jl`](#advanced-installation-of-parallelkdejl) section below before running the following command.

`ParallelKDEpy` can be imported with:

```python
import parallelkdepy as pkde
```

The first time that `ParallelKDEpy` is imported, it will automatically download `Julia` and `ParallelKDE.jl`. During the process, you will be prompted to provide your GitHub username and password (or personal token) to authenticate the installation since `ParallelKDE.jl` is still a private repository.

### Advanced installation of `ParallelKDE.jl`
Since `ParallelKDE.jl` is still a private repository, CI of `ParallelKDEpy` requires the `main` and `dev` branches to refer to a locally cloned version of `ParallelKDE.jl`. In order to work with wrapper, any cloned branch from `main` or `dev` need to have the `url` entry in the `src/parallelkdepy/juliapkg.json` file changed as follows:

```json
{
  "julia": "^1.11",
  "packages": {
    "ParallelKDE": {
      "uuid": "251f600b-d60c-4092-b1b9-465b74160c73",
      "url": "https://github.com/chrissm23/ParallelKDE.jl",
      "rev": "main"  # or "dev" for the latest changes
    }
  }
}
```

For quickly applying and testing changes to `ParallelKDE.jl` it is recommended to follow its installation [instructions](https://github.com/chrissm23/ParallelKDE.jl) and, before importing the wrapper for the first time, change the file `url` entry in `src/parallelkdepy/juliapkg.json` to point to the local path of `ParallelKDE.jl`.

> [!NOTE]
> Remember to omit the changes to the `juliapkg.json` file from the git index, so that it does not get committed to the repository. This can be done by running the following command in the root directory of `ParallelKDEpy`:

```bash
git update-index --skip-worktree /path/to/ParallelKDEpy/src/parallelkdepy/juliapkg.json
```

## Usage
`ParallelKDE` can be executed using the python wrapper as follows:

```python
import parallelkdepy as pkde

# Grids can be generated with a sequence of tuples (coord_min, coord_max, n_points), e.g., for n_dims dimensions
ranges = [(coord_min, coord_max, n_points)] * n_dims
grid = pkde.Grid(ranges=ranges, device="cpu")
grid_coordinates = grid.to_meshgrid() # Creates a tuple of numpy arrays containing the coordinates of each dimension

# Assume that `data` contains a 2D numpy array with dimensions (n_samples, n_dims)
"""
- There are two possible devices 'cpu' and 'cuda'.
- Setting grid=True will automatically find an appropriate grid for the data but a specific grid can be given as well.
  If a `Grid` is provided, its device must match the device of the `DensityEstimation`
"""
density_estimation = pkde.DensityEstimation(
  data, grid=True, device="cpu"
)
# The grid can be obtained with:
grid = density_estimation.get_grid()

"""
Other keyword arguments of `estimate_density` are:
- `time_step`: Time step of propagation.
- `n_steps`: Number of time steps for propagation. Defaults to 1000. Only one of `time_step` or `n_steps` should be specified.
- `n_bootstraps`: Number of bootstraps to perform. Defaults to 100.
- `eps1`: Threshold of first derivative as stopping criterion for the propagation. Defaults to 1.5.
- `eps2`: Threshold of second derivative as stopping criterion for the propagation. Defaults to 0.1 (CPU) or 1.0 (CUDA).
- `smoothness_duration`: fraction of the total time to require smoothness before entering the next propagation regime. Defaults to 0.005 (0.5%).
- `stable_duration`: fraction of the total time to require stability before entering the stopping propagation. Defaults to 0.01 (1%).
"""
density_estimation.estimate_density("parallelEstimator") # So far it's the only estimator implemented

density_estimated = density_estimation.get_density()

# For convenience, the Dirac sequence for the data can be generated ushing a `Grid` with
# - The Dirac sequence can also be initialized in either "cpu" or "cuda"
dirac_sequence = pkde.initialize_dirac_sequence(data, grid, device="cpu")
```

## Contributing
For contributions of specific features or bug fixes to this wrapper, please open an issue in the [ParallelKDEpy repository](https://github.com/chrissm23/ParallelKDEpy/issues) or create a pull request to the [dev](https://github.com/chrissm23/ParallelKDEpy/tree/dev) branch.
