from pathlib import Path

from .text import TM1TextFile


class TM1LogFile(TM1TextFile):
    """
    A class representation of a tm1 log file

    """

    suffix = "log"

    def __init__(self, path: Path):

        super().__init__(path)


class TM1ChangeLogFile(TM1LogFile):
    """
    A class representation of a tm1s log file

    """

    def __init__(self, path: Path):

        super().__init__(path)

    # to avoid opening this file, which may throw an error, override these methods
    # Not sure if this is the best approach, can maybe output a warning

    def read(self):
        pass

    def write(self, text):
        pass

    def _get_encoding(self):
        pass

    def _get_non_empty(self):
        pass
