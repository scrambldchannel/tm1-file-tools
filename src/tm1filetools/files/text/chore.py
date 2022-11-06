from pathlib import Path

from .text import TM1TextFile


class TM1ChoreFile(TM1TextFile):
    """
    A class representation of a tm1 TI process file

    """

    suffix = "cho"

    def __init__(self, path: Path):

        super().__init__(path)

    # A chore is just a text file that holds a name, processes to run and params, and scheduling information
