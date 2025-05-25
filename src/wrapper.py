"""
High-level API: Functions and objects that wrap Julia calls.
"""

from .core import _init_julia  # add more things needed from the low level API
import numpy as np

# initialize Julia once
_init_julia()


class DensityEstimation:
    """
    Main API object for density estimation.

    Attributes
    ----------

    Methods
    -------
    """

    def __init__(self) -> None:
        pass
