from .binary import TM1BinaryFile


class TM1DimensionFile(TM1BinaryFile):
    """
    A class representation of a tm1 dim file
    """

    suffix = "dim"

    def __init__(self, path):

        super().__init__(path)


class TM1AttributeDimensionFile(TM1DimensionFile):
    """
    A class representation of a tm1 dimension attribute dim file
    """

    prefix = f"{TM1BinaryFile.attribute_prefix}"

    def __init__(self, path):

        super().__init__(path)


# Other control dimensions exist, this is not a full list
