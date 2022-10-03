from pathlib import Path

import chardet

from ..base import TM1File


class TM1TextFile(TM1File):
    """
    Base class for TM1 text files (rux, pro, vue etc)

    """

    def __init__(self, path: Path):

        super().__init__(path)

        # this introduces a dependency and may not really be useful
        with open(self._path, "rb") as f:
            data = f.read()
            self.encoding = chardet.detect(data)["encoding"]

    def read(self):
        with open(self._path, "r") as f:
            return f.read()

    def write(self, text):
        with open(self._path, "w") as f:
            f.write(text)
