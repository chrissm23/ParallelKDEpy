"""
A quick runnable example of using ParallelKDEpy.
"""

# TODO: Mark this directory as runnable in README

import numpy as np
import matplotlib.pyplot as plt
from parallelkdepy import estimate_kde


def main():
    # generate synthetic data
    data = np.concatenate(
        [np.random.normal(-2, 0.5, 500), np.random.normal(3, 1.0, 500)]
    )
    # estimate KDE
    grid, density = estimate_kde(data, bandwidth=0.7)
    # plot result
    plt.plot(grid, density)
    plt.title("ParallelKDEpy Estimate")
    plt.xlabel("x")
    plt.ylabel("density")
    plt.show()


if __name__ == "__main__":
    main()
