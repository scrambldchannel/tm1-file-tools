from pathlib import Path


class TM1File:
    """
    Base class for TM1 files
    """

    prefix = ""
    suffix = None
    control_prefix = "}"

    # suffixes (incomplete, all lower case, not sure what default is)
    suffixes = {
        "cube_suffix": "cub",
        "dimension_suffix": "dim",
        "subset_suffix": "sub",
        "view_suffix": "vue",
        "ti_suffix": "pro",
        "rule_prefix": "rux",
        "blb_suffix": "blb",
        "cma_suffix": "cma",
        # ...
    }

    def __init__(self, path):

        self._path = Path(path)
        self.name = self._path.name
        self.stem = self._path.stem
        # Potentially flags files that aren't TM1 artifacts based on suffix
        # Seems an elegant way to drop the "."
        self.suffix = self._path.suffix.split(".")[1]
        # Set the prefix
        self.prefix = None
        self.is_control = self._is_control_object()

    def exists(self):

        return self._path.exists()

    def _is_control_object(self):

        return self.stem[0] == self.control_prefix

    # could easily be an attribute I suppose
    def is_tm1_file(self):

        # special files
        if self.name.lower() == "tm1s.cfg":
            return True

        return any(s.lower() == self.suffix.lower() for s in self.suffixes.values())

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
