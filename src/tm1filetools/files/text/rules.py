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

        with open(self._path, "r") as f:

            for row in f:

                row = row.strip().lower()

                if self._is_terminated(row) and row[:-1].rstrip() == "skipcheck":

                    return True

        return False

    def has_feeders(self):

        with open(self._path, "r") as f:

            for row in f:

                row = row.strip().lower()

                if self._is_terminated(row) and row[:-1].rstrip() == "feeders":

                    return True

        return False

    @classmethod
    def _is_terminated(cls, row: str):

        row = row.strip()

        # having removed the guff at the end, I'm hoping this should

        if len(row) > 0:
            return row if row[-1] == ";" else False
