import glob


class TM1FileTool:
    """
    Base class for TM1 file tool object

    """

    def __init__(self, path=None):
        # Can be initialised with a path but also without to access class methods
        self._path = path

    @classmethod
    def case_insensitive_glob(cls, pattern):
        def either(c):
            return "[%s%s]" % (c.lower(), c.upper()) if c.isalpha() else c

        return glob.glob("".join(map(either, pattern)))

    @classmethod
    def get_name_part(cls, name: str) -> str:
        """
        Returns just the name part of a pathname (stem?)
        Is there maybe a built in function of the path object that does this?
        """

        return name.split("/")[-1].split(".")[0]
