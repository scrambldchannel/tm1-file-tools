from .binary import TM1BinaryFile


class TM1CubeFile(TM1BinaryFile):
    """
    A class representation of a tm1 cube file
    """

    def __init__(self, path):

        super().__init__(path)

        # what else?
        # public view path? Whether views exist?
