import glob

# simplify API in files/__init.py__ ?
from tm1filetools.files.base import TM1File


class TM1FileTool:
    """
    TM1 file tool object

    """

    # static properties
    # etc....
    # Case?
    cell_security_prefix = TM1File.control_prefix + "CellSecurity_"
    picklist_prefix = TM1File.control_prefix + "Picklist_"
    drill_prefix = TM1File.control_prefix + "Drill_"
    annotations_prefix = TM1File.control_prefix + "ElementAnnotations_"

    def __init__(self, path=None):
        # Should we initialise via path to cfg file instead?
        self._path = path

    # def get_orphan_ruxes(self):
    #     """
    #     Return orphaned rux files
    #     """
    #     return self._get_orphans(object_ext="cub", artifact_ext="rux")

    # def get_orphan_attr_dims(self):
    #     """
    #     Return orphaned attribute dim files - i.e. a
    #     """
    #     return self._get_orphans(object_ext="dim", artifact_ext="dim", artifact_prefix=self.attr_prefix)

    # def _get_orphans(
    #     self, object_ext: str, artifact_ext: str, artifact_prefix: str = "", strip_prefix=True
    # ) -> List[str]:
    #     """
    #     Return a list of orphaned artifacts
    #     """

    #     objects = self._get_files(ext=object_ext)
    #     artifacts = self._get_files(ext=artifact_ext, prefix=artifact_prefix, strip_prefix=strip_prefix)

    #     return [a for a in artifacts if a not in objects]

    # def get_ruxes(self) -> List[str]:
    #     """
    #     Returns all rux file names
    #     """

    #     return self._get_files(ext="rux")

    # def _get_files(self, ext: str, prefix: str = "") -> List[str]:
    #     """
    #     Returns all files with specified ext and optional prefix within the path
    #     """

    #     files = self._case_insensitive_glob(f"{self._path}/{prefix}*.{ext}")

    #     files = [self._get_name_part(f, strip_suffix=strip_suffix) for f in files]

    #     return files

    @staticmethod
    def _case_insensitive_glob(pattern: str):
        # I still don't find this that transparent

        def either(c):
            return "[%s%s]" % (c.lower(), c.upper()) if c.isalpha() else c

        return glob.glob("".join(map(either, pattern)))
