from ..base import TM1File


class TM1BinaryFile(TM1File):
    """
    Base class for TM1 binary files (cub, dim etc)

    """

    def __init__(self, path):

        super().__init__(path)
