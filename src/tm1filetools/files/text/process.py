from pathlib import Path

from .linecode import TM1LinecodeFile


class TM1ProcessFile(TM1LinecodeFile):
    """
    A class representation of a tm1 TI process file

    """

    suffix = "pro"

    def __init__(self, path: Path):

        super().__init__(path)

    # There's scope to do some naive "parsing" of the text
    # and potentially even create a tool for hot promotion using TM1py
