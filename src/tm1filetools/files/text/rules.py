from pathlib import Path

from .text import TM1TextFile


class TM1RulesFile(TM1TextFile):
    """
    A class representation of a tm1 rule file (rux)

    """

    suffix = "rux"
    block_terminator = ";"

    def __init__(self, path: Path):

        super().__init__(path)

    def has_skipcheck(self):

        for row in self.reader():

            row = row.strip().lower()

            if self._is_terminated(row) and row[:-1] == "skipcheck":

                return True

        return False

    def has_feeders(self):

        for row in self.reader():

            row = row.strip().lower()
            if self._is_terminated(row) and row[:-1] == "feeders":

                return True

            return False

    @staticmethod
    def _is_terminated(row: str):

        row = row.strip()

        # having removed the guff at the end, I'm hoping this should
        return row
