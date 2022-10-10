from pathlib import Path

from .text import TM1TextFile


class TM1RulesFile(TM1TextFile):
    """
    A class representation of a tm1 rulea file (rux)

    """

    suffix = "rux"

    def __init__(self, path: Path):

        super().__init__(path)
