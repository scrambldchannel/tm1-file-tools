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
        self.is_non_empty = self._get_non_empty()
        self.encoding = self._get_encoding()

        self.f = None

    # unsure of what the best approach is here
    # looking at the way the reader function works
    # in e.g. the csv module, it takes a file
    # (or some sort of iterable) as an argument
    # this is ultimately done in c 
    # @classmethod
    # def reader(f, rstrip: bool = True):

    #     for row in f:
    #         # do I ever not want to strip the newline char?

    #         if rstrip:
    #             yield row.rstrip()
    #         else:
    #             yield row

    def read(self):
        with open(self._path, "r") as f:
            return f.read()

    def readlines(self):
        with open(self._path, "r") as f:
            return [line.rstrip() for line in f]

    def write(self, text):
        with open(self._path, "w") as f:
            f.write(text)

        self.is_non_empty = self._get_non_empty()

    def _get_encoding(self):

        if self.exists():
            with open(self._path, "rb") as f:
                data = f.read()
                return chardet.detect(data)["encoding"]

        return None

    def _get_non_empty(self):

        if self.exists():
            return self._path.stat().st_size > 0

        return False
