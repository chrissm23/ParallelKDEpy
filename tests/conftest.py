import pytest
import numpy as np

import parallelkdepy as pkde


@pytest.fixture(params=[1, 2, 3], ids=lambda x: f"{x}D")
def n_dims(request):
    """
    Fixture to provide a number of dimensions for testing.

    Parameters
    ----------
    request : pytest.FixtureRequest
        The request object for the fixture.

    Returns
    -------
    int
        The number of dimensions to use in tests.
    """
    return request.param


@pytest.fixture(params=["cpu", "cuda"], ids=lambda x: f"device_{x}")
def device(request):
    """
    Fixture to provide a device type for testing.

    Parameters
    ----------
    request : pytest.FixtureRequest
        The request object for the fixture.

    Returns
    -------
    str
        The device type to use in tests, e.g., 'cpu' or 'cuda'.
    """
    return request.param


@pytest.fixture
def generate_grid(n_dims, device) -> pkde.Grid:
    """
    Fixture to generate a grid for testing.

    Parameters
    ----------
    n_dims : int
        The number of dimensions for the grid.
    device : str
        The device type to use for the grid.

    Returns
    -------
    Grid
        A Grid object initialized with the specified number of dimensions and device.
    """
    ranges = [(-1.0, 1.0, 100)] * n_dims
    return pkde.Grid(ranges=ranges, device=device)


@pytest.fixture
def generate_data(n_dims) -> np.ndarray:
    """
    Fixture to generate random data for testing.

    Parameters
    ----------
    n_dims : int
        The number of dimensions for the data.

    Returns
    -------
    np.ndarray
        A numpy array of shape (1000, n_dims) with random values.
    """
    return np.random.normal(scale=0.9, size=(1000, n_dims))


@pytest.fixture
def generate_density_estimation(generate_data, device) -> pkde.DensityEstimation:
    """
    Fixture to create a DensityEstimation object for testing.

    Parameters
    ----------
    generate_data : np.ndarray
        The data to use for density estimation.
    generate_grid : Grid
        The grid on which to perform density estimation.
    device : str
        The device type to use for the density estimation.

    Returns
    -------
    DensityEstimation
        A DensityEstimation object initialized with the provided data and grid.
    """
    return pkde.DensityEstimation(
        generate_data,
        grid=True,
        device=device,
    )
