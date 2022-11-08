import itertools
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

    def __str__(self):

        return f"{self.__class__.__name__} ({self.name})"

    def exists(self):

        return self._path.exists()

    def _is_control_object(self):

        return self.stem[0] == self.control_prefix

    def _get_suffix(self):

        return self._path.suffix[1:]

    def delete(self) -> int:
        """Deletes this file

        Returns:
            count of files deleted

        """

        # How best to do exception handling?
        self._path.unlink()

        return 1

    # i.e. rename the stem part, not the suffix or the parent
    # probably most useful for renaming cubes, dims, views and subsets in advance of a restart
    def rename(self, new_name: str):

        # I feel there must be a more elegant way to do this
        new_path = Path.joinpath(self._path.parent, f"{new_name}.{self.suffix}")
        self._path = self._path.rename(new_path)

        # This could lead to some confusion about the difference b/w stem and name :shrug:
        # Maybe there's a better way to handle this but let's just update the attribute
        self.stem = self._path.stem

    def rename_suffix_to_lower(self):

        # a way to standardise all file extensions to lower case
        new_path = Path.joinpath(self._path.parent, f"{self._stem}.{self._path.suffix.lower()}")
        self._path = self._path.rename(new_path)

    def strip_prefix(self):

        return self.stem.removeprefix(self.prefix)

    @staticmethod
    def _get_suffix_permutations(suffix: str):

        lu_sequence = ((c.lower(), c.upper()) for c in suffix)
        return ["".join(x) for x in itertools.product(*lu_sequence)]


class NonTM1File(TM1File):

    # Kind of a stupid name

    def __init__(self, path):

        super().__init__(path)

        self.is_control = False
        self.is_tm1_file = False
