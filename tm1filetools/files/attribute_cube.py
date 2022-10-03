from .cube import TM1CubeFile


class TM1AttributeCubeFile(TM1CubeFile):
    """
    A class representation of a tm1 attribute cube file
    """

    # is this right?
    prefix = f"{TM1CubeFile.control_prefix}ElementAttributes_"

    def __init__(self, path):

        super().__init__(path)
