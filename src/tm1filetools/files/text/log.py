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

        return "_".join(self.stem.split("_")[2:])

    def _get_timestamp(self):

        return self.stem.split("_")[1]


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
