import glob
from typing import List


class TM1FileTool:
    """
    Base class for TM1 file tool object

    """

    # static properties

    control_prefix = "}"
    attr_prefix = control_prefix + "ElementAttributes_"
    # etc....
    # Case?
    cell_security_prefix = control_prefix + "CellSecurity_"
    picklist_prefix = control_prefix + "Picklist_"
    drill_prefix = control_prefix + "Drill_"
    annotations_prefix = control_prefix + "ElementAnnotations_"

    def __init__(self, path=None):
        # Can be initialised with a path but also without to access class methods
        self._path = path

    def get_orphan_ruxes(self):
        """
        Return orphaned rux files
        """
        return self._get_orphans(object_ext="cub", artifact_ext="rux")

    def _get_orphans(self, object_ext: str, artifact_ext: str) -> List[str]:
        """
        Return a list of orphaned artifacts
        """

        objects = self._get_files_by_ext(ext=object_ext)
        artifacts = self._get_files_by_ext(ext=artifact_ext)

        return [a for a in artifacts if a not in objects]

    def get_blbs(self) -> List[str]:
        """
        Returns all blb file names
        """

        return self._get_files_by_ext(ext="blb")

    def get_ruxes(self) -> List[str]:
        """
        Returns all rux file names
        """

        return self._get_files_by_ext(ext="rux")

    def get_dims(self) -> List[str]:
        """
        Returns all dim file names
        """

        return self._get_files_by_ext(ext="dim")

    def get_vues(self) -> List[str]:
        """
        Returns all vue file names
        """

        return self._get_files_by_ext(ext="vue")

    def get_subs(self) -> List[str]:
        """
        Returns all sub file names
        """

        return self._get_files_by_ext(ext="sub")

    def get_cubs(self) -> List[str]:
        """
        Returns all cub file names
        """

        return self._get_files_by_ext(ext="cub")

    def get_attr_dims(self) -> List[str]:
        """
        Return all attribute dimension names
        """

        return self._get_files_by_ext(ext="dim", prefix=self.attr_prefix)

    def get_attr_cubs(self) -> List[str]:
        """
        Return all attribute cube names
        """

        return self._get_files_by_ext(ext="cub", prefix=self.attr_prefix)

    def _get_files_by_ext(self, ext: str, prefix: str = "") -> List[str]:
        """
        Returns all files with specified ext and optional prefix within the path
        """

        return [self._get_name_part(a) for a in self._case_insensitive_glob(f"{self._path}/{prefix}*.{ext}")]

    @staticmethod
    def _case_insensitive_glob(pattern: str):
        # I still don't find this that transparent

        def either(c):
            return "[%s%s]" % (c.lower(), c.upper()) if c.isalpha() else c

        return glob.glob("".join(map(either, pattern)))

    @staticmethod
    def _get_name_part(name: str) -> str:
        """
        Returns just the name part of a pathname (stem?)
        Is there maybe a built in function of the path object that does this?
        """

        return name.split("/")[-1].split(".")[0]
