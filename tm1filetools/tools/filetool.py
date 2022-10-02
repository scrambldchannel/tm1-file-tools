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

    def get_orphan_attr_dims(self):
        """
        Return orphaned attribute dim files - i.e. a
        """
        return self._get_orphans(object_ext="dim", artifact_ext="dim", artifact_prefix=self.attr_prefix)

    def _get_orphans(
        self, object_ext: str, artifact_ext: str, artifact_prefix: str = "", strip_prefix=True
    ) -> List[str]:
        """
        Return a list of orphaned artifacts
        """

        objects = self._get_files(ext=object_ext)
        artifacts = self._get_files(ext=artifact_ext, prefix=artifact_prefix, strip_prefix=strip_prefix)

        return [a for a in artifacts if a not in objects]

    def get_blbs(self) -> List[str]:
        """
        Returns all blb file names
        """

        return self._get_files(ext="blb")

    def get_ruxes(self) -> List[str]:
        """
        Returns all rux file names
        """

        return self._get_files(ext="rux")

    def get_dims(self) -> List[str]:
        """
        Returns all dim file names
        """

        return self._get_files(ext="dim")

    def get_vues(self) -> List[str]:
        """
        Returns all vue file names
        """

        return self._get_files(ext="vue")

    def get_subs(self) -> List[str]:
        """
        Returns all sub file names
        """

        return self._get_files(ext="sub")

    def get_cubs(self) -> List[str]:
        """
        Returns all cub file names
        """

        return self._get_files(ext="cub")

    def get_attr_dims(self) -> List[str]:
        """
        Return all attribute dimension names
        """

        return self._get_files(ext="dim", prefix=self.attr_prefix)

    def get_attr_cubs(self) -> List[str]:
        """
        Return all attribute cube names
        """

        return self._get_files(ext="cub", prefix=self.attr_prefix)

    def _get_files(self, ext: str, prefix: str = "", strip_prefix=False, strip_suffix=True) -> List[str]:
        """
        Returns all files with specified ext and optional prefix within the path
        """

        files = self._case_insensitive_glob(f"{self._path}/{prefix}*.{ext}")

        files = [self._get_name_part(f, strip_suffix=strip_suffix) for f in files]

        if strip_prefix:
            files = [f.removeprefix(prefix) for f in files]

        return files

    @staticmethod
    def _case_insensitive_glob(pattern: str):
        # I still don't find this that transparent

        def either(c):
            return "[%s%s]" % (c.lower(), c.upper()) if c.isalpha() else c

        return glob.glob("".join(map(either, pattern)))

    @staticmethod
    def _get_name_part(name: str, strip_suffix=True) -> str:
        """
        Returns just the name part of a pathname (stem?)
        There must be an existing implementation of something like this
        """

        if strip_suffix:
            return name.split("/")[-1].split(".")[0]
        else:
            return name.split("/")[-1]
