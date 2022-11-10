from pathlib import Path
from typing import List, Optional

from tm1filetools.files.text.log import (
    TM1ChangeLogFile,
    TM1LogFile,
    TM1ProcessErorrLogFile,
)

from .base import TM1BaseFileTool


class TM1LogFileTool(TM1BaseFileTool):
    """
    TM1 log file tool class

    """

    # this can be moved to a parent class or something
    suffixes = [
        TM1LogFile.suffix,
    ]

    def __init__(self, path: Path):

        self._path: Path = path

        self._path = path

        # logs - can be split into categories
        self._log_files: Optional[list] = None

    def find_all(self):
        """
        Do a full scan of the dir(s) and populate all lists of files
        """

        self._find_logs()

    def get_logs(self) -> List[TM1LogFile]:
        """Returns list of all log files

        Returns:
            List of log files
        """

        if self._log_files is None:
            self._find_logs()

        return self._log_files

    def _find_logs(self):

        # logs may be in a different path so search with the glob func
        # We should also be careful of the tm1s.log file as we may fail to get a lock on it

        logs = []
        for log in self._case_insensitive_glob(self._path, f"*.{TM1LogFile.suffix}"):
            # if we think this is the tm1s.log file, use the derived class that avoids trying to open it
            if log.stem.lower() == "tm1s":
                logs.append(TM1ChangeLogFile(log))
            elif log.stem.lower().startswith(TM1ProcessErorrLogFile.prefix.lower()):
                logs.append(TM1ProcessErorrLogFile)
            else:
                logs.append(TM1LogFile(log))

        self._log_files = logs