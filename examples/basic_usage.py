"""
A quick example of using ParallelKDEpy.
"""

import numpy as np
import matplotlib.pyplot as plt

import os

import parallelkdepy as pkde


def main():
    data = np.random.randn(10000, 1)  # Generate random data

    density_estimation = pkde.DensityEstimation(
        data,
        grid=True,
        device="cpu",
    )
    density_estimation.estimate_density("gradepro")

    density_estimated = density_estimation.get_density()
    grid_coordinates = density_estimation.generate_grid().to_meshgrid()[0]

    density_true = np.exp(-0.5 * grid_coordinates**2) / np.sqrt(2 * np.pi)

    plt.plot(
        grid_coordinates, density_true, label="True Density", lw=2, c="cornflowerblue"
    )
    plt.plot(
        grid_coordinates,
        density_estimated,
        label="Estimated Density",
        lw=2,
        c="firebrick",
    )
    plt.xlabel("Random Variable")
    plt.ylabel("Density")
    plt.legend()
    plt.grid()

    plt.savefig(
        os.path.join(os.path.dirname(__file__), "basic_usage.png"),
        dpi=300,
        bbox_inches="tight",
    )


if __name__ == "__main__":
    main()
