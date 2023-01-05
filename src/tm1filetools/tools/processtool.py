from pathlib import Path
from typing import List

from tm1filetools.files.text.process import TM1ProcessFile

from .base import TM1BaseFileTool


class TM1ProcessFileTool(TM1BaseFileTool):
    """
    TM1 process file tool class

    """

    suffix = TM1ProcessFile.suffix

    def __init__(self, path: Path):

        self._path: Path = path

    def _files(self, model=True, control=False):
        """
        A generator that returns all processs with filters applied
        """

        for proc in self._case_insensitive_glob(self._path, f"*.{self.suffix}"):

            process_file = TM1ProcessFile(proc)

            if not model and not process_file.is_control:
                continue

            if not control and process_file.is_control:
                continue

            yield process_file

    def get_all(self) -> List[TM1ProcessFile]:
        """Returns a list of all the process files found

        Returns:
            List of process files
        """

        return [c for c in self._files(control=True)]

    def get_all_model(self) -> List[TM1ProcessFile]:
        """Returns a list of all the model process files found

        Returns:
            List of process files
        """

        return [r for r in self._files()]

    def get_all_control(self) -> List[TM1ProcessFile]:
        """Returns a list of all the model process files found

        Returns:
            List of process files
        """

        return [r for r in self._files(model=False, control=True)]
