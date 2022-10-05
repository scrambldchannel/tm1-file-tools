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
        self.encoding = self._get_encoding()

    def read(self):
        with open(self._path, "r") as f:
            return f.read()

    def write(self, text):
        with open(self._path, "w") as f:
            f.write(text)

    def _get_encoding(self):

        # Check if exists?
        with open(self._path, "rb") as f:
            data = f.read()
            return chardet.detect(data)["encoding"]
