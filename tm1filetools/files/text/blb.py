from pathlib import Path

from .text import TM1TextFile


class TM1BLBFile(TM1TextFile):
    """
    A class representation of a tm1 BLB file

    """

    suffix = "blb"

    def __init__(self, path: Path):

        super().__init__(path)
