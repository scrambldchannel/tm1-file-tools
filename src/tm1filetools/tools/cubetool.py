from pathlib import Path
from typing import List, Union

from tm1filetools.files.binary.cube import (
    TM1AttributeCubeFile,
    TM1CellSecurityCubeFile,
    TM1CubeFile,
)

from .base import TM1BaseFileTool


class TM1CubeFileTool(TM1BaseFileTool):
    """
    TM1 cube file tool class

    """

    suffix = TM1CubeFile.suffix

    def __init__(self, path: Path):

        self._path: Path = path

    def get_all(self) -> List[Union[TM1CubeFile, TM1AttributeCubeFile, TM1CellSecurityCubeFile]]:
        """Returns a list of all the cube files found

        Returns:
            List of cube files
        """

        return [c for c in self._files(control=True)]

    def get_all_attr(self) -> List[TM1AttributeCubeFile]:
        """Returns list of all attribute cube files

        Returns:
            List of attribute cube files
        """

        return [
            # I'm also sort of repeating this condition twice...
            self._determine_cube_type(c)
            for c in self._files(model=False, control=True)
            if c.name.startswith(TM1AttributeCubeFile.attribute_prefix)
        ]

    def get_all_model(self) -> List[TM1CubeFile]:
        """Returns a list of all the model cube files found

        Returns:
            List of cube files
        """

        # no need to check, these will always be normal cubes
        return [TM1CubeFile(c) for c in self._files()]

    def get_all_control(self) -> List[Union[TM1CubeFile, TM1AttributeCubeFile, TM1CellSecurityCubeFile]]:
        """Returns a list of all the model cube files found

        Returns:
            List of cube files
        """

        return [self._determine_cube_type(c) for c in self._files(model=False, control=True)]

    @staticmethod
    def _determine_cube_type(c):

        # obviously need to add further logic if we want to use more subclasses
        if c.stem.startswith(TM1AttributeCubeFile.attribute_prefix):

            return TM1AttributeCubeFile(c)

        else:
            return TM1CubeFile(c)
