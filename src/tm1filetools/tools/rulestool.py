from pathlib import Path
from typing import List

from tm1filetools.files.text.rules import TM1RulesFile

from .base import TM1BaseFileTool


class TM1RulesFileTool(TM1BaseFileTool):
    """
    TM1 rules file tool class

    """

    suffix = TM1RulesFile.suffix

    def __init__(self, path: Path):

        self._path: Path = path

    def get_all(self) -> List[TM1RulesFile]:
        """Returns a list of all the rules files found

        Returns:
            List of rules files
        """

        return [TM1RulesFile(r) for r in self._files(control=True)]

    def get_all_model(self) -> List[TM1RulesFile]:
        """Returns a list of all the model rules files found

        Returns:
            List of rules files
        """

        return [TM1RulesFile(r) for r in self._files()]

    def get_all_control(self) -> List[TM1RulesFile]:
        """Returns a list of all the model rules files found

        Returns:
            List of rules files
        """

        return [TM1RulesFile(r) for r in self._files(model=False, control=True)]
