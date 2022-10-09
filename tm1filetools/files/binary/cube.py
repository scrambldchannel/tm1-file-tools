from .binary import TM1BinaryFile


class TM1CubeFile(TM1BinaryFile):
    """
    A class representation of a tm1 cube file
    """

    suffix = "cub"

    def __init__(self, path):

        super().__init__(path)


class TM1AttributeCubeFile(TM1CubeFile):
    """
    A class representation of a tm1 attribute cube file
    """

    prefix = f"{TM1BinaryFile.attribute_prefix}"

    def __init__(self, path):

        super().__init__(path)


class TM1CellSecurityCubeFile(TM1CubeFile):
    """
    A class representation of a tm1 cell security cube file
    """

    prefix = f"{TM1CubeFile.control_prefix}CellSecurity_"

    def __init__(self, path):

        super().__init__(path)


class TM1PicklistCubeFile(TM1CubeFile):
    """
    A class representation of a tm1 picklist cube file
    """

    prefix = f"{TM1CubeFile.control_prefix}Picklist_"

    def __init__(self, path):

        super().__init__(path)


# This is not an exhaustive list
# Some others we could add are:

# }Drill_
# }ElementAnnotations_
# Other security objects (probably higher value)
# etc ...
