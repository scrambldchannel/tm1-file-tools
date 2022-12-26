import csv
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


class TM1ChangeLogFile(TM1LogFile):
    """
    A class representation of a tm1s log file

    """

    metadata_prefix = "#"
    delimiter = ","
    quote = '"'

    def __init__(self, path: Path):

        super().__init__(path)

    def reader(self):

        if self._path.exists:
            with open(self._path, "r") as f:
                for row in csv.reader(self._discard_metadata(f), delimiter=self.delimiter, quotechar=self.quote):
                    yield row

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
