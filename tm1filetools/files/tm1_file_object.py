from pathlib import Path


class TM1FileObject:
    """
    Represents a file in the TM1 data directory

    I need to migrate functionality to this class or similar
    """

    def __init__(self, path: Path):

        self.path = path
        self.name = path.stem
        self.object_type = path.suffix.lower()
        self.control = self.name[0] == "}"

    def __gt__(self, other):
        return self.name > other.name
