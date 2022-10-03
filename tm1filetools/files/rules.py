from pathlib import Path

from .text import TM1TextFile


class TM1RulesFile(TM1TextFile):
    """
    A class representation of a tm1 rulea file (rux)

    """

    suffix = "rux"

    def __init__(self, path: Path):

        super().__init__(path)

        self.cube_path = self._get_cube_path()

    def _get_cube_path(self):

        return Path.joinpath(self._path.parent, f"{self._path.stem}.cub")

    def is_orphan(self):

        return not self._get_cube_path().exists()
