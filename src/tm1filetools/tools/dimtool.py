from pathlib import Path
from typing import List, Union

from tm1filetools.files.binary.dimension import (
    TM1AttributeDimensionFile,
    TM1DimensionFile,
)

from .base import TM1BaseFileTool


class TM1DimensionFileTool(TM1BaseFileTool):
    """
    TM1 dimension file tool class

    """

    # this can be moved to a parent class or something
    suffix = TM1DimensionFile.suffix

    def __init__(self, path: Path):

        self._path: Path = path

    def get_all(self) -> List[Union[TM1DimensionFile, TM1AttributeDimensionFile]]:
        """Returns a list of all the dim files found

        Returns:
            List of dim files
        """

        return [c for c in self._files(control=True)]

    def get_all_attr(self) -> List[TM1AttributeDimensionFile]:
        """Returns list of all attribute dim files

        Returns:
            List of attribute dimension files
        """

        return [
            # I'm also sort of repeating this condition twice...
            self._determine_dim_type(d)
            for d in self._files(model=False, control=True)
            if d.name.startswith(TM1AttributeDimensionFile.attribute_prefix)
        ]

    def get_all_model(self) -> List[TM1DimensionFile]:
        """Returns a list of all the model dim files found

        Returns:
            List of cube files
        """

        return [TM1DimensionFile(d) for d in self._files()]

    def get_all_control(self) -> List[Union[TM1DimensionFile, TM1AttributeDimensionFile]]:
        """Returns a list of all the control dim files found

        Returns:
            List of dim files
        """

        return [self._determine_dim_type(d) for d in self._files(model=False, control=True)]

    @staticmethod
    def _determine_dim_type(d):

        # obviously need to add further logic if we want to use more subclasses
        if d.stem.startswith(TM1AttributeDimensionFile.attribute_prefix):

            return TM1AttributeDimensionFile(d)

        else:
            return TM1DimensionFile(d)
