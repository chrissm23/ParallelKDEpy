import matplotlib
from pathlib import Path

matplotlib.use("Agg")  # Use a non-interactive backend for plotting

# [docs-start]
import numpy as np
import matplotlib.pyplot as plt
import parallelkdepy as pkde

data = np.random.normal(size=(10000, 1))  # Example data: 10000 samples in 1D

density_estimation = pkde.DensityEstimation(
    data,
    grid=True,
    device="cpu",
)
density_estimation.estimate_density("gradepro")

density_estmated = density_estimation.get_density()
grid_coordinates = density_estimation.generate_grid().to_meshgrid()[0]

# Evaluate true density for comparison
density_true = np.exp(-0.5 * grid_coordinates**2) / np.sqrt(2 * np.pi)

plt.plot(grid_coordinates, density_true, label="True Density", lw=2, c="cornflowerblue")
plt.plot(
    grid_coordinates, density_estmated, label="Estimated Density", lw=2, c="firebrick"
)
plt.xlabel("Random Variable")
plt.ylabel("Density")
plt.legend()
plt.grid()
# [docs-end]

out = (
    Path(__file__).resolve().parents[1] / "_static" / "figures" / "getting-started.png"
)
out.parent.mkdir(parents=True, exist_ok=True)
plt.savefig(out, bbox_inches="tight", dpi=300)
plt.close()
