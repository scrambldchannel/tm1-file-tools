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

    def _files(self, model=True, control=False):
        """
        A generator that returns all dimensions with filters applied
        """

        for cub in self._case_insensitive_glob(self._path, f"*.{TM1DimensionFile.suffix}"):

            dim_file = TM1DimensionFile(cub)

            if not model and not dim_file.is_control:
                continue

            if not control and dim_file.is_control:
                continue

            # attempt to derive subclass

            if dim_file.name.startswith(TM1AttributeDimensionFile.attribute_prefix):

                yield TM1AttributeDimensionFile(cub)

            else:

                yield dim_file

    def get_all_dims(self) -> List[Union[TM1DimensionFile, TM1AttributeDimensionFile]]:
        """Returns a list of all the dim files found

        Returns:
            List of dim files
        """

        return [c for c in self._files(control=True)]

    def get_attr_dims(self) -> List[TM1AttributeDimensionFile]:
        """Returns list of all attribute dim files

        Returns:
            List of attribute dimension files
        """

        return [
            # I'm also sort of repeating this condition twice...
            c
            for c in self._files(model=False, control=True)
            if c.name.startswith(TM1AttributeDimensionFile.attribute_prefix)
        ]

    def get_model_dims(self) -> List[TM1DimensionFile]:
        """Returns a list of all the model dim files found

        Returns:
            List of cube files
        """

        return [d for d in self._files()]

    def get_control_dims(self) -> List[Union[TM1DimensionFile, TM1AttributeDimensionFile]]:
        """Returns a list of all the control dim files found

        Returns:
            List of dim files
        """

        return [c for c in self._files(model=False, control=True)]

    def get_orphan_attr_dims(self) -> List[TM1AttributeDimensionFile]:
        """Returns list of attribute dim files that don't have corresponding dim files

        Returns:
            List of attribute dim files
        """

        return [
            a
            for a in self.get_attr_dims()
            if a.strip_prefix().lower() not in [d.stem.lower() for d in self.get_all_dims()]
        ]
