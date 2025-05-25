"""
Low-level plumbing: Manage Julia session and interfacing between Python and Julia.
"""

from juliacall import Main as jl

_initialized = False


def _init_julia():
    global _initialized
    if not _initialized:
        jl.seval("using ParallelKDE")
        _initialized = True
