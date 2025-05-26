"""
High-level API: Functions and objects that wrap Julia calls.
"""

from typing import Sequence, Self, Optional

from . import core
import numpy as np

# initialize Julia once
core._init_julia()


class Grid:
    """
    Higer level implementation of a grid to use over meshgrid.

    Attributes
    ----------
    grid_jl : juliacall.AnyValue
        Underlying Julia grid object.
    device : str
        Device type, e.g., 'cpu' or 'cuda'.
    shape : tuple
        Shape of the grid.

    Methods
    -------
    get_coordinates()
        Returns the coordinates of the grid.
    step()
        Returns the step size of the grid.
    bounds()
        Returns the bounds of the grid.
    lower_bounds()
        Returns the lower bounds of the grid.
    higher_bounds()
        Returns the higher bounds of the grid.
    initiial_bandwidth()
        Returns the minimum bandwidth that the grid can support.
    fftgrid()
        Returns a grid of frequency components.
    """

    def __init__(
        self,
        ranges: Sequence[tuple] = [],
        *,
        device: str = "cpu",
        b32: Optional[bool] = None,
        grid_jl=None,
    ) -> None:
        if grid_jl is None:
            if (ranges is None) or (len(ranges) == 0):
                raise ValueError("Ranges must be provided to create a grid.")

            grid_jl = core.create_grid(ranges, device=device, b32=b32)

            self._grid_jl = grid_jl
            self._device = device
            self._shape = core.grid_shape(grid_jl)
        else:
            self._grid_jl = grid_jl
            self._device = core.grid_device(grid_jl)
            self._shape = core.grid_shape(grid_jl)

    @property
    def grid_jl(self):
        """
        Underlying Julia grid object.
        """
        return self._grid_jl

    @property
    def device(self) -> str:
        """
        Device type, e.g., 'cpu' or 'cuda'.
        """
        return self._device

    @property
    def shape(self) -> tuple:
        """
        Shape of the grid.
        """
        return self._shape

    def to_meshgrid(self) -> tuple[np.ndarray, ...]:
        """
        Mesh grid coordinates
        """
        return core.grid_coordinates(self._grid_jl)

    def step(self) -> list:
        """
        List of step sizes for each dimension of the grid.
        """
        return core.grid_step(self._grid_jl)

    def bounds(self) -> list[tuple]:
        """
        List of tuples of bounds for each dimension of the grid.
        """
        return core.grid_bounds(self._grid_jl)

    def lower_bounds(self) -> list:
        """
        List of lower bounds for each dimension of the grid.
        """
        return [lb for lb, _ in self.bounds()]

    def higher_bounds(self) -> list:
        """
        List of lower bounds for each dimension of the grid.
        """
        return [hb for _, hb in self.bounds()]

    def initial_bandwidth(self) -> list:
        """
        List of the minimum bandwidth that the grid can support in each dimension.
        """
        return core.grid_initial_bandwidth(self._grid_jl)

    def fftgrid(self):
        """
        Returns a grid of frequency components.
        """
        return Grid(grid_jl=core.grid_fftgrid(self._grid_jl))


def initialize_dirac_sequence(
    data: np.ndarray,
    grid: Grid,
    bootstrap_indices: Optional[np.ndarray] = None,
    device: str = "cpu",
    method: str = "serial",
) -> np.ndarray:
    """
    Initialize a Dirac sequence on the given grid.

    Parameters
    ----------
    data : np.ndarray
        Data points to initialize the Dirac sequence.
    grid : Grid
        The grid on which to initialize the Dirac sequence.

    Returns
    -------
    np.ndarray
        Numpy array representing the initialized Dirac sequence.
    """
    return core.initialize_dirac_sequence(
        data, grid.grid_jl, bootstrap_indices, device, method
    )


class DensityEstimation:
    """
    Main API object for density estimation.

    Attributes
    ----------
    data : np.ndarray
        Numpy array of data points for density estimation. Shape should be (n_samples, n_features).
    density : np.ndarray
        Numpy array representing the estimated density.
    grid : Optional[Grid]
        The grid on which the density is estimated if required by the method.
    device : str
        Device type, e.g., 'cpu' or 'cuda'.
    _densityestimation_jl : juliacall.AnyValue
        Underlying Julia density estimation object.

    Methods
    -------
    generate_grid
        Generates a grid based on the data and specified parameters.
    estimate_density
        Uses the specified method to estimate the density from the data.
    """

    def __init__(
        self,
        data: np.ndarray,
        grid: Grid | bool = False,
        dims: Optional[Sequence] = None,
        grid_bounds: Optional[Sequence] = None,
        grid_padding: Optional[Sequence] = None,
        device: str = "cpu",
    ) -> None:
        self._data = data
        self._device = device

        if isinstance(grid, Grid):
            if grid.device != device:
                raise ValueError(
                    f"Grid device {grid.device} does not match DensityEstimation device {device}."
                )
            self._grid = grid
        elif grid is True:
            self._grid = Grid(
                grid_jl=core.find_grid(data, dims, grid_bounds, grid_padding, device)
            )
        elif grid is False:
            self._grid = None
        else:
            raise ValueError(
                "Grid must be a Grid object, True to find a grid, or False to not use a grid."
            )

        if self._grid is not None:
            self._densityestimation_jl = core.create_density_estimation(
                data, grid=self._grid.grid_jl, device=device
            )
        else:
            self._densityestimation_jl = core.create_density_estimation(
                data, device=device
            )
        self._density = core.get_density(self._densityestimation_jl)

    @property
    def data(self) -> np.ndarray:
        """
        Numpy array of data points for density estimation.
        """
        return self._data

    @property
    def device(self) -> str:
        """
        Device type, e.g., 'cpu' or 'cuda'.
        """
        return self._device

    @property
    def grid(self) -> Optional[Grid]:
        """
        Returns the grid used for density estimation, if any.
        """
        return self._grid

    @property
    def density(self) -> np.ndarray:
        """
        Numpy array representing the estimated density.
        """
        return self.get_density()

    def generate_grid(
        self,
        dims: Optional[Sequence] = None,
        grid_bounds: Optional[Sequence] = None,
        grid_padding: Optional[Sequence] = None,
    ) -> Grid:
        """
        Generates a grid based on the data and specified parameters.

        Returns
        -------
        Grid
            A Grid object representing the generated grid.
        """
        return Grid(
            grid_jl=core.find_grid(
                self.data, dims, grid_bounds, grid_padding, self.device
            )
        )

    def estimate_density(self, estimation: str, **kwargs) -> None:
        """
        Executes the density estimation algorithm on the data.
        """
        core.estimate_density(self._densityestimation_jl, estimation, **kwargs)

    def get_density(self) -> np.ndarray:
        """
        Returns the estimated density as a Numpy array.
        """
        return core.get_density(self._densityestimation_jl)
