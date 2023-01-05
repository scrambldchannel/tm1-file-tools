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

    def _files(self, model=True, control=False):
        """
        A generator that returns all ruless with filters applied
        """

        for rux in self._case_insensitive_glob(self._path, f"*.{self.suffix}"):

            rules_file = TM1RulesFile(rux)

            if not model and not rules_file.is_control:
                continue

            if not control and rules_file.is_control:
                continue

            yield rules_file

    def get_all_rules(self) -> List[TM1RulesFile]:
        """Returns a list of all the rules files found

        Returns:
            List of rules files
        """

        return [c for c in self._files(control=True)]

    def get_model_rules(self) -> List[TM1RulesFile]:
        """Returns a list of all the model rules files found

        Returns:
            List of rules files
        """

        return [r for r in self._files()]

    def get_control_rules(self) -> List[TM1RulesFile]:
        """Returns a list of all the model rules files found

        Returns:
            List of rules files
        """

        return [r for r in self._files(model=False, control=True)]
