from .dimension import TM1DimensionFile


class TM1AttributeDimensionFile(TM1DimensionFile):
    """
    A class representation of a tm1 dimension attribute dim file
    """

    prefix = f"{TM1DimensionFile.control_prefix}ElementAttributes_"

    def __init__(self, path):

        super().__init__(path)

        # what else?
        # public subsets path? Whether subsets exist?
        # Presumably this binary file is also where all the hierarchy info lives?
