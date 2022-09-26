import glob


def get_name_part(full_name: str) -> str:
    """
    Returns just the name part of a pathname (stem?)
    Is there maybe a built in function of the path object that does this?
    """

    return full_name.split("/")[-1].split(".")[0]


def case_insensitive_glob(pattern):
    def either(c):
        return "[%s%s]" % (c.lower(), c.upper()) if c.isalpha() else c

    return glob.glob("".join(map(either, pattern)))
