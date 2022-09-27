import glob


class TM1FileTool:
    """
    Base class for TM1 file tool object

    """

    # static properties

    control_prefix = "}"
    attr_prefix = "}ElementAttributes_"
    # etc....

    def __init__(self, path=None):
        # Can be initialised with a path but also without to access class methods
        self._path = path

    @staticmethod
    def _case_insensitive_glob(pattern: str):
        # I still don't find this that transparent
        # is there a library that takes care of this maybe?

        def either(c):
            return "[%s%s]" % (c.lower(), c.upper()) if c.isalpha() else c

        return glob.glob("".join(map(either, pattern)))

    @staticmethod
    def _get_name_part(name: str) -> str:
        """
        Returns just the name part of a pathname (stem?)
        Is there maybe a built in function of the path object that does this?
        """

        return name.split("/")[-1].split(".")[0]
