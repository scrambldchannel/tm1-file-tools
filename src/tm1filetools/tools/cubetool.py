from pathlib import Path
from typing import List, Union

from tm1filetools.files.binary.cube import TM1CellSecurityCubeFile  # noqa
from tm1filetools.files.binary.cube import TM1PicklistCubeFile  # noqa
from tm1filetools.files.binary.cube import TM1AttributeCubeFile, TM1CubeFile

from .base import TM1BaseFileTool


class TM1CubeFileTool(TM1BaseFileTool):
    """
    TM1 cube file tool class

    """

    # this can be moved to a parent class or something
    suffix = TM1CubeFile.suffix

    def __init__(self, path: Path):

        self._path: Path = path

    def _files(self, model=True, control=False):
        """
        A generator that returns all cubes with filters applied
        """

        for cub in self._case_insensitive_glob(self._path, f"*.{TM1CubeFile.suffix}"):

            cube_file = TM1CubeFile(cub)

            if not model and not cube_file.is_control:
                continue

            if not control and cube_file.is_control:
                continue

            # attempt to derive subclass

            if not cube_file.is_control:

                yield cube_file

            elif cube_file.name.startswith(TM1AttributeCubeFile.attribute_prefix):

                yield TM1AttributeCubeFile(cub)

    def get_all_cubes(self) -> List[Union[TM1CubeFile, TM1AttributeCubeFile, TM1CellSecurityCubeFile]]:
        """Returns a list of all the cube files found

        Returns:
            List of cube files
        """

        return [c for c in self._files(control=True)]

    def get_attr_cubes(self) -> List[TM1AttributeCubeFile]:
        """Returns list of all attribute cube files

        Returns:
            List of attribute cube files
        """

        return [
            # I'm also sort of repeating this condition twice...
            c
            for c in self._files(model=False, control=True)
            if c.name.startswith(TM1AttributeCubeFile.attribute_prefix)
        ]

    def get_model_cubes(self) -> List[TM1CubeFile]:
        """Returns a list of all the model cube files found

        Returns:
            List of cube files
        """

        return [c for c in self._files()]

    def get_control_cubes(self) -> List[Union[TM1CubeFile, TM1AttributeCubeFile, TM1CellSecurityCubeFile]]:
        """Returns a list of all the model cube files found

        Returns:
            List of cube files
        """

        return [c for c in self._files(model=False, control=True)]

    def get_orphan_attr_cubes(self):
        """Returns list of attribute cube files that don't have corresponding dim files

        Returns:
            List of cube files
        """

        return [
            a
            for a in self.cubes.get_attr_cubes()
            if a.strip_prefix().lower() not in [d.stem.lower() for d in self.get_dims(control=True)]
        ]
