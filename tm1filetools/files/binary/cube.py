from .binary import TM1BinaryFile


class TM1CubeFile(TM1BinaryFile):
    """
    A class representation of a tm1 cube file
    """

    suffix = "cub"

    def __init__(self, path):

        super().__init__(path)

        # what else?
        # public view path? Whether views exist?


class TM1AttributeCubeFile(TM1CubeFile):
    """
    A class representation of a tm1 attribute cube file
    """

    # is this right?
    prefix = f"{TM1CubeFile.control_prefix}{TM1BinaryFile.attribute_prefix}"

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


# Not really sure there's any value in the below
# Review and possibly remove

# class TM1DrillCubeFile(TM1CubeFile):
#     """
#     A class representation of a tm1 drill cube file
#     """

#     prefix = f"{TM1CubeFile.control_prefix}Drill_"

#     def __init__(self, path):

#         super().__init__(path)

# class TM1AnnotationsCubeFile(TM1CubeFile):
#     """
#     A class representation of a tm1 annotations cube file
#     """

#     prefix = f"{TM1CubeFile.control_prefix}ElementAnnotations_"

#     def __init__(self, path):

#         super().__init__(path)
