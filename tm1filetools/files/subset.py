from pathlib import Path

from .text import TM1TextFile


class TM1SubsetFile(TM1TextFile):
    """
    A class representation of a tm1 view file

    """

    def __init__(self, path: Path, public: bool = True):

        super().__init__(path)

        self.cube = self._get_cube_name()
        self.public = public
        self.owner = self._get_owner_name()
        # subset_name maybe a clearer API than stem?
        self.subset_name = self.stem

    def move_to_public(self) -> None:

        if self.public:
            # raise a warning?
            return None

        # what to do if a public view with same name already exists?
        # Will throw an error on windows...
        new_path = Path.joinpath(self._get_public_subsets_path(), self.name)
        self._path = self._path.replace(new_path)
        self.public = True

    def _get_cube_name(self) -> str:

        return self._path.parent.stem.removesuffix("}subs")

    def _get_owner_name(self) -> str:

        return None if self.public else self._path.parent.parent.stem

    def _get_public_subsets_path(self) -> str:

        # Is this useful in any other context other than moving to the public folder?
        if self.public:
            return self._path.parent

        # otherwise remove the user folder from the parent tree
        return Path.joinpath(self._path.parents[2], self._path.parents[0].stem)
