# import glob

# simplify API in files/__init.py__ ?
from pathlib import Path, PureWindowsPath, WindowsPath

# from tm1filetools.files.base import TM1File
from tm1filetools.files import TM1CfgFile, TM1CubeFile, TM1DimensionFile, TM1RulesFile


class TM1FileTool:
    """
    TM1 file tool object

    """

    def __init__(self, path: Path, local: bool = False):

        self._path: Path = path

        # local means the code is running on the machine the folder exists
        # this means that an absolute path in the cfg file can be used
        self._local = local

        self.config_file = self._get_config_file()

        # if we do have a config file, attempt to derive paths to logs, data etc
        self.data_path = self._get_data_path_from_cfg()

        self.dimension_files = self._get_dims()
        self.cube_files = self._get_cubes()
        self.cube_rules = self._get_rules()

    def _get_dims(self):
        """
        Returns a list of all dim file objects
        """
        return [TM1DimensionFile(d) for d in self._get_files_by_suffix(TM1DimensionFile.suffix)]

    def _get_cubes(self):

        return [TM1CubeFile(c) for c in self._get_files_by_suffix(TM1CubeFile.suffix)]

    def _get_rules(self):

        return [TM1RulesFile(r) for r in self._get_files_by_suffix(TM1RulesFile.suffix)]

    def _get_files_by_suffix(self, suffix: str):

        return self._case_insensitive_glob(self.data_path, f"*.{suffix}")

    def _get_config_file(self):

        cfg_file_path = next(self._case_insensitive_glob(path=self._path, pattern="tm1s.cfg"), None)

        if cfg_file_path:
            return TM1CfgFile(cfg_file_path)

        return None

    def _get_data_path_from_cfg(self):

        if not self.config_file:
            return self._path

        # need to read the data directory from the config file
        # which may be relative or absolute
        # a further complexity might be that the code is running on a different
        # OS to one where this tm1s.cfg file comes from...
        # for now, I'm going to assume this is a windows path

        data_dir = self.config_file.get_parameter("DataBaseDirectory")

        if data_dir:
            # Note, this is the 90% case
            # I can't find any details on how this parameter might look
            # with TM1 running on *nix, nor do I have much understanding
            pure_path = PureWindowsPath(data_dir)

            if pure_path.is_absolute():

                if self._local:
                    return WindowsPath(pure_path)
                # there are ways we could make an educated guess here but it's probably
                # more trouble than it's worth
                return None
            else:
                # thanks to the magic of pathlib, this seems to work cross platform :)
                # note, I've made it an absolute path, not sure this is strictly necessary
                # It does make writing a test a bit easier
                return Path.joinpath(self._path, pure_path).resolve()

        return self._path

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
    def _case_insensitive_glob(path: Path, pattern: str):
        # I still don't find this that transparent

        def either(c):
            return "[%s%s]" % (c.lower(), c.upper()) if c.isalpha() else c

        return path.glob("".join(map(either, pattern)))
