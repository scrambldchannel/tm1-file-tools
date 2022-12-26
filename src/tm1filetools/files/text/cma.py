import csv
from pathlib import Path

from .text import TM1TextFile


class TM1CMARow:
    def __init__(self, row):

        """Representation of a single line in the cma file"""

        # afaik, each row will have a fixed number of columns, based on the cube
        self.row = row


class TM1CMAFile(TM1TextFile):
    """
    A class representation of a tm1 CMA file

    TM1 creates files with a cma extension that are really csv files containing exports of cube data

    """

    suffix = "cma"
    # does this vary?
    quote_character = '"'

    def __init__(self, path: Path):

        super().__init__(path)

        self.delimiter = self._get_delimiter()
        self.cube = self._get_cube()

    def _get_delimiter(self):

        if not self.is_non_empty:
            return None

        # This is a bit janky but if we assume the first column is a quoted string
        # the delimiter will be the first character after the second quote

        # read the first line of the file
        with self._path.open() as f:

            line = f.readline()
            index = line.find(self.quote_character, 1) + 1
            return line[index]

    def _get_cube(self):

        if not self.is_non_empty:
            return None

        with self._path.open() as f:

            line = f.readline()
            index = line.find(self.quote_character, 1)
            return line[1:index]

    # do I really want to write to these files?
    def write(self, text):

        super().write(text)

        self.delimiter = self._get_delimiter()
        self.cube = self._get_cube()

    def reader(self, control: bool = False, cube: str = None, user: str = None, dt: str = None):
        """
        A generator that reads each line of the cma and yields every row matching the applied filters

        """

        if self._path.exists:
            with open(self._path, "r") as f:
                for row in csv.reader(f, delimiter=self.delimiter, quotechar=self.quote_character):

                    row_obj = TM1CMARow(row)

                    # if dt and row_obj.dt.lower() != dt.lower():
                    #     continue

                    yield row_obj
