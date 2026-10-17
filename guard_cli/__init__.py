"""Guard: Graph-powered safety layer for AI coding agents."""
from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("guard-cli")
except PackageNotFoundError:
    __version__ = "0.1.2"
