"""Public package API for mujocohelper."""

from importlib.metadata import PackageNotFoundError, version
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .renderer import Renderer

try:
    __version__ = version("mujocohelper")
except PackageNotFoundError:
    __version__ = "0.0.0"

__all__ = ["Renderer", "__version__"]


def __getattr__(name: str):
    if name == "Renderer":
        from .renderer import Renderer

        return Renderer
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
