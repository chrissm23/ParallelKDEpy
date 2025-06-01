import functools

import numpy as np
import pytest

import parallelkdepy as pkde


def test_grid(generate_grid, n_dims, device):
    ranges = [(-1.0, 1.0, 100)] * n_dims

    assert generate_grid.device == device
    assert generate_grid.shape == (100,) * n_dims

    range_np = np.linspace(-1.0, 1.0, num=100)
    mesh = np.meshgrid(*[range_np for _ in range(n_dims)], indexing="ij")
    grid_mesh = generate_grid.to_meshgrid()
    for i in range(n_dims):
        assert np.allclose(grid_mesh[i], mesh[i])

    assert np.allclose(generate_grid.step(), [np.diff(range_np)[0]] * n_dims)
    assert generate_grid.bounds() == [(r[0], r[1]) for r in ranges]
    assert generate_grid.lower_bounds() == [r[0] for r in ranges]
    assert generate_grid.upper_bounds() == [r[1] for r in ranges]
    assert np.allclose(
        generate_grid.initial_bandwidth(), [np.diff(range_np)[0] / 2] * n_dims
    )

    grid_fft = generate_grid.fftgrid()
    fft_range = 2 * np.pi * np.fft.fftfreq(100, d=np.diff(range_np)[0])
    mesh_fft = np.meshgrid(*[fft_range for _ in range(n_dims)], indexing="ij")
    grid_fft_mesh = grid_fft.to_meshgrid()
    for i in range(n_dims):
        assert np.allclose(grid_fft_mesh[i], mesh_fft[i])


def test_dirac(generate_grid, n_dims, device):
    data = np.zeros((1, n_dims))
    dirac_sequences = pkde.initialize_dirac_sequence(data, generate_grid, device=device)

    density = np.zeros((100,) * n_dims)

    range_np = np.linspace(-1.0, 1.0, num=100)
    spacing_squared = np.diff(range_np)[0] ** (2 * n_dims)

    remainder_l = np.full(n_dims, np.diff(range_np)[0] / 2)
    remainder_h = np.full(n_dims, np.diff(range_np)[0] / 2)

    vals = [np.array([remainder_l[i], remainder_h[i]]) for i in range(n_dims)]
    products = functools.reduce(np.multiply.outer, vals)

    sequence_terms = products / spacing_squared
    idx_list = [[49, 50]] * n_dims
    density[np.ix_(*idx_list)] += sequence_terms

    assert np.allclose(dirac_sequences[0].real, density)


def test_density_estimation(generate_density_estimation, generate_data, n_dims, device):
    assert generate_density_estimation.device == device
    assert np.allclose(generate_density_estimation.data, generate_data)

    grid_found = generate_density_estimation.grid
    density_estimation2 = pkde.DensityEstimation(
        generate_data, dims=grid_found.shape, device=device
    )
    assert density_estimation2.generate_grid() == grid_found

    assert np.all(
        (generate_data[:, i] >= grid_found.lower_bounds()[i])
        & (generate_data[:, i] <= grid_found.upper_bounds()[i])
        for i in range(generate_data.shape[1])
    )

    grid_new = pkde.Grid([(-5.0, 5.0, 100)] * n_dims, device=device)
    generate_density_estimation.grid = grid_new
    assert generate_density_estimation.grid == grid_new
    assert generate_density_estimation.generate_grid() == grid_new

    generate_density_estimation.generate_grid(dims=(500,) * n_dims, overwrite=True)
    assert generate_density_estimation.grid.shape == (500,) * n_dims


# TODO: Extend this test to cover more dimensions
@pytest.mark.parametrize("n_dims", [1], indirect=True)
def test_estimation_result(generate_density_estimation, generate_pdf):
    generate_density_estimation.estimate_density("parallelEstimator")
    density_estimated = generate_density_estimation.get_density()

    dx = np.prod(generate_density_estimation.generate_grid().step())
    n_gridpoints = np.prod(generate_density_estimation.generate_grid().shape)
    mise = np.sum(density_estimated - generate_pdf) ** 2 * dx / n_gridpoints

    # TODO: Replace with appropriate MISE threshold
    assert mise < 0.01
