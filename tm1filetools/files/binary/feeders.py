from .binary import TM1BinaryFile


class TM1FeedersFile(TM1BinaryFile):
    """
    A class representation of a tm1 feeders file
    """

    suffix = "feeders"

    def __init__(self, path):

        super().__init__(path)
