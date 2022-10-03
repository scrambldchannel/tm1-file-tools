from pathlib import Path

from .base import TM1File


class TM1TextFile(TM1File):
    """
    Base class for TM1 text files (rux, pro, vue etc)

    """

    def __init__(self, path: Path):
        # do I need to do this or should I just not override the init?
        super().__init__(path)

    def read(self):
        with open(self._path, "r") as f:
            return f.read()

    def write(self, text):
        with open(self._path, "w") as f:
            f.write(text)
