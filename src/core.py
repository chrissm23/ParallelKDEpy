"""
Low-level plumbing: Manage Julia session and direct Pkg calls.
"""

from juliacall import Main as jl

_initialized = False


def _init_julia():
    global _initialized
    if not _initialized:
        # TODO: Install julia if it isn't and load or activate ParallelKDE.jl
        _initialized = True
