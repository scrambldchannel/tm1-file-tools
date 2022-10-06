from pathlib import Path


class TM1File:
    """
    Base class for TM1 files
    """

    prefix = ""
    control_prefix = "}"
    is_tm1_file = True

    def __init__(self, path):

        self._path = Path(path)
        self.name = self._path.name
        self.stem = self._path.stem
        self.is_control = self._is_control_object()
        self.suffix = self._get_suffix()

    def exists(self):

        return self._path.exists()

    def _is_control_object(self):

        return self.stem[0] == self.control_prefix

    def _get_suffix(self):

        return self._path.suffix[1:]

    def delete(self):

        return self._path.unlink()

    # i.e. rename the stem part, not the suffix or the parent
    # probably most useful for renaming cubes, dims, views and subsets in advance of a restart
    def rename(self, new_name: str):

        # I feel there must be a more elegant way to do this
        new_path = Path.joinpath(self._path.parent, f"{new_name}.{self.suffix}")
        self._path = self._path.rename(new_path)

        # This could lead to some confusion about the difference b/w stem and name :shrug:
        # Maybe there's a better way to handle this but let's just update the attribute
        self.stem = self._path.stem


class NonTM1File(TM1File):

    # Kind of a stupid name

    def __init__(self, path):

        super().__init__(path)

        self.is_control = False
        self.is_tm1_file = False
