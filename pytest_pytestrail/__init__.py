# coding: utf-8
from . import pytestrail

try:
    from .__version__ import version as __version__
except ImportError:
    __version__ = "unknown"

__all__ = ["pytestrail", "__version__"]
