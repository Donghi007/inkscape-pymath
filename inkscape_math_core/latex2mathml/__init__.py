try:
    from importlib import metadata
    __version__ = metadata.version("latex2mathml")
except Exception:
    __version__ = "3.81.0"
