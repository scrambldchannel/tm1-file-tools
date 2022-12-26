import csv

# from datetime import datetime
from pathlib import Path

from .text import TM1TextFile


class TM1LogFile(TM1TextFile):
    """
    A class representation of a tm1 log file

    """

    suffix = "log"

    def __init__(self, path: Path):

        super().__init__(path)


class TM1ProcessErorrLogFile(TM1LogFile):
    """
    A class representation of a tm1s TI process error log file

    """

    prefix = "TM1ProcessError_"

    def __init__(self, path: Path):

        super().__init__(path)

        self.process = self._get_process_name()
        self.timestamp = self._get_timestamp()

    def _get_process_name(self):

        #
        return "_".join(self.stem.split("_")[2:])

    def _get_timestamp(self):

        return self.stem.split("_")[1]


class TM1ChangeLogRow:
    def __init__(self, row):

        """Representation of a single line in the transaction log"""

        # parse the line and set properties
        self.time = row[1]
        self.cube = row[7]
        self.user = row[3]
        self.dt = row[4].upper()
        # elements start at idx 8 until the end but there seems to
        # always be an empty col at the end :shrug:
        self.elements = row[8:-1]
        self.el_count = len(self.elements) + 1
        self._old_val = row[5]
        self._new_val = row[6]

        if self.dt == "N":
            self.old_val_n = float(self._old_val)
            self.new_val_n = float(self._new_val)
            self.delta = self.new_val_n - self.old_val_n
            self.abs_delta = abs(self.delta)

        # shouldn't have any other types
        else:
            # not sure the casting is necessary
            self.old_val_s = str(self._old_val)
            self.new_val_s = str(self._new_val)


class TM1ChangeLogFile(TM1LogFile):
    """
    A class representation of a tm1s log file

    """

    metadata_prefix = "#"
    delimiter = ","
    quote = '"'

    def __init__(self, path: Path):

        super().__init__(path)

    def reader(self, control: bool = False, cube: str = None, user: str = None, dt: str = None):
        """
        A generator that reads each line of the log and yields every row matching the applied filters

        """
        if self._path.exists:
            with open(self._path, "r") as f:
                for row in csv.reader(self._discard_metadata(f), delimiter=self.delimiter, quotechar=self.quote):

                    row_obj = TM1ChangeLogRow(row)

                    # apply filters
                    if cube:
                        control = True
                        # implies include control
                        if row_obj.cube.lower() != cube.lower():
                            continue

                    if not control and row_obj.cube[0] == "}":
                        continue

                    if user and row_obj.user.lower() != user.lower():
                        continue

                    if dt and row_obj.dt.lower() != dt.lower():
                        continue

                    yield row_obj

    def get_cubes(self, control: bool = False):

        cubes = set()

        for row in self.reader(control=control):

            cubes.add(row.cube)

        return cubes

    def get_users(self, control: bool = False):

        users = set()

        for row in self.reader(control=control):

            users.add(row.user)

        return users

    @classmethod
    def _discard_metadata(cls, f):

        # The intent here is to create a wrapper for a file object that discards
        # the metadata lines in a change log file
        for row in f:

            if len(row) < 3:
                continue

            first_char = row.removeprefix(" ")[0]

            if first_char == cls.metadata_prefix:
                continue
            else:
                yield row
