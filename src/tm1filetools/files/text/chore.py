from pathlib import Path

from .linecode import TM1LinecodeFile


class TM1ChoreFile(TM1LinecodeFile):
    """
    A class representation of a tm1 TI process file

    """

    suffix = "cho"

    def __init__(self, path: Path):

        super().__init__(path)

    # A chore is just a text file that holds a name, processes to run and params, and scheduling information
