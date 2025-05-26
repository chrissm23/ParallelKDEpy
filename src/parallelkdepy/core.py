"""
Low-level plumbing: Manage Julia session and interfacing between Python and Julia.
"""

from typing import Sequence, Optional

import numpy as np

from juliacall import Main as jl

_initialized = False


def _init_julia():
    global _initialized

    if not _initialized:
        jl.seval("using ParallelKDE")
        _initialized = True


AvailableDevices = {
    jl.ParallelKDE.IsCPU: "cpu",
    jl.ParallelKDE.IsCUDA: "cuda",
}


def create_grid(ranges: Sequence, device: str = "cpu", b32: Optional[bool] = None):
    """
    Create a grid instance of the Julia object `ParallelKDE.Grid`.

    Parameters
    ----------
    ranges : Sequence
        The ranges for the grid.
    device : str, optional
        The device type, e.g., 'cpu' or 'cuda'. Default is 'cpu'.
    b32 : Optional[bool], optional
        Whether to use 32-bit precision for CUDA devices.
        Default is None, which uses 32-bit precision if the device is 'cuda'.
    Returns
    -------
    juliacall.AnyValue
        The created grid object in Julia.
    """
    ranges = [jl.range(start, stop, length) for start, stop, length in ranges]
    if device == "cpu":
        grid = jl.initialize_grid(*ranges)
    elif device == "cuda":
        if b32 is None:
            grid = jl.initialize_grid(*ranges, device=device, b32=True)
        else:
            grid = jl.initialize_grid(*ranges, device=device, b32=b32)
    else:
        raise ValueError(f"Unsupported device type: {device}")

    return grid


def grid_shape(grid_jl) -> tuple:
    return jl.size(grid_jl)


def grid_device(grid_jl) -> str:
    device_jl = jl.ParallelKDE.get_device(grid_jl)
    try:
        return AvailableDevices[device_jl]
    except KeyError:
        raise ValueError(f"Unsupported device type: {device_jl}")


def grid_coordinates(grid_jl) -> tuple[np.ndarray, ...]:
    coords_np = jl.get_coordinates(grid_jl).to_numpy()

    return tuple(coords_np[i, ...] for i in range(coords_np.shape[0]))


def grid_step(grid_jl) -> list:
    return list(jl.spacings(grid_jl))


def grid_bounds(grid_jl) -> list[tuple]:
    bounds_np = jl.bounds(grid_jl).to_numpy()

    return list(zip(bounds_np[0], bounds_np[1]))


def grid_initial_bandwidth(grid_jl) -> list:
    return list(jl.initial_bandwidth(grid_jl))


def grid_fftgrid(grid_jl):
    return jl.fftgrid(grid_jl)


def initialize_dirac_sequence(
    data: np.ndarray,
    grid_jl,
    bootstrap_indices: Optional[np.ndarray] = None,
    device: str = "cpu",
    method: str = "serial",
) -> np.ndarray:
    """
    Creates a numpy array with the dirac sequence obtained from the data on the grid.

    Parameters
    ----------
    data : np.ndarray
        Numpy array of the data with shape (n_samples, n_features).
    grid_jl
        Julia grid object.
    bootstrap_indices : Optional[np.ndarray], optional
        Optional numpy array of bootstrap indices. If provided, it should have shape (n_bootstraps, n_samples).
    device : str, optional
        The device to store the array, e.g., 'cpu' or 'cuda'. Default is 'cpu'.
    method : str, optional
        The method to use for initializing the Dirac sequence, e.g., 'serial' or 'parallel'. Default is 'serial'.
    """
