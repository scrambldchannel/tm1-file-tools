from pathlib import Path

from .text import TM1TextFile


class TM1UserFile(TM1TextFile):
    """
    A base class for files that get created (and may be owned) by users
    That is, views and subsets.
    You probably don't want to instantiate this class, use view or subset instead
    """

    def __init__(self, path: Path, public: bool = True):

        super().__init__(path)

        self.public = public
        self.owner = self._get_owner_name()

    def move_to_public(self) -> None:

        if self.public:
            # raise a warning?
            return None

        # what to do if a public file with same name already exists?
        # Will throw an error on windows...
        new_path = Path.joinpath(self._get_public_path(), self.name)
        self._path = self._path.replace(new_path)
        self.public = True

    def _get_object_name(self) -> str:

        return self._path.parent.stem.removesuffix(self.folder_suffix)

    def _get_owner_name(self) -> str:

        return None if self.public else self._path.parent.parent.stem

    def _get_public_path(self) -> str:

        # Is this useful in any other context other than moving to the public folder?
        if self.public:
            return self._path.parent

        # otherwise remove the user folder from the parent tree
        return Path.joinpath(self._path.parents[2], self._path.parents[0].stem)
