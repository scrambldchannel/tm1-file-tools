# simplify API in files/__init.py__ ?
from pathlib import Path, PureWindowsPath, WindowsPath

# from tm1filetools.files.base import TM1File
from tm1filetools.files import (
    NonTM1File,
    TM1AttributeCubeFile,
    TM1AttributeDimensionFile,
    TM1CfgFile,
    TM1CMAFile,
    TM1CubeFile,
    TM1DimensionFile,
    TM1FeedersFile,
    TM1LogFile,
    TM1ProcessFile,
    TM1RulesFile,
    TM1SubsetFile,
    TM1ViewFile,
)


class TM1FileTool:
    """
    TM1 file tool object

    """

    suffixes = [
        TM1CfgFile.suffix,
        TM1CubeFile.suffix,
        TM1DimensionFile.suffix,
        TM1ProcessFile.suffix,
        TM1RulesFile.suffix,
        TM1SubsetFile.suffix,
        TM1ViewFile.suffix,
        TM1CMAFile.suffix,
        TM1FeedersFile.suffix,
    ]

    def __init__(self, path: Path, local: bool = False):

        self._path: Path = path

        # local means the code is running on the machine the folder exists
        # this means that an absolute path in the cfg file can be used
        self._local = local

        self.config_file = self._find_config_file()

        # if we do have a config file, attempt to derive paths to logs, data etc
        self.data_path = self._get_data_path_from_cfg()

        # scan for all file types
        self._scan_all()

    def re_scan(self):

        self._scan_all()

    def delete(self, file_object):

        file_object.delete()

        self._scan_all()

    def delete_all_feeders(self):

        for fd in self.feeders_files:
            fd.delete()

        self.feeders_files = self._find_feeders()

    def delete_all_orphans(self):

        self.delete_orphan_rules()
        self.delete_orphan_attr_dims()
        self.delete_orphan_attr_cubes()
        self.delete_orphan_views()
        self.delete_orphan_subsets()
        self.delete_orphan_feeders()

    def delete_orphan_rules(self):

        for r in self.get_orphan_rules():
            r.delete()

        self.rules_files = self._find_rules()

    def delete_orphan_attr_dims(self):

        for d in self.get_orphan_attr_dims():
            d.delete()

        self.dim_files = self._find_dims()

    def delete_orphan_attr_cubes(self):

        for c in self.get_orphan_attr_cubes():
            c.delete()

        self.cube_files = self._find_cubes()

    def delete_orphan_views(self):

        for v in self.get_orphan_views():
            v.delete()

        self.view_files = self._find_views()

    def delete_orphan_subsets(self):

        for s in self.get_orphan_subsets():
            s.delete()

        self.sub_files = self._find_subs()

    def delete_orphan_feeders(self):

        for f in self.get_orphan_feeders():
            f.delete()

        self.feeders_files = self._find_feeders()

    def get_model_cubes(self):

        return [c for c in self.cube_files if not c.is_control]

    def get_model_dimensions(self):

        return [d for d in self.dim_files if not d.is_control]

    def get_control_cubes(self):

        return [c for c in self.cube_files if c.is_control]

    def get_control_dimensions(self):

        return [d for d in self.dim_files if d.is_control]

    def get_control_processes(self):

        return [p for p in self.process_files if p.is_control]

    def get_control_views(self):

        return [v for v in self.view_files if v.is_control]

    def get_control_subsets(self):

        return [s for s in self.sub_files if s.is_control]

    def get_attr_cubes(self):

        return [TM1AttributeCubeFile(c._path) for c in self.cube_files if c.name.find(c.attribute_prefix) == 0]

    def get_attr_dimensions(self):

        return [
            TM1AttributeDimensionFile(d._path)
            for d in self.dim_files
            if d.name.lower().find(d.attribute_prefix.lower()) == 0
        ]

    def get_orphan_rules(self):

        return [r for r in self.rules_files if r.stem.lower() not in [c.stem for c in self.cube_files]]

    def get_orphan_attr_dims(self):

        return [
            a
            for a in self.get_attr_dimensions()
            if a.strip_prefix().lower() not in [d.stem.lower() for d in self.dim_files]
        ]

    def get_orphan_attr_cubes(self):

        return [
            a for a in self.get_attr_cubes() if a.strip_prefix().lower() not in [d.stem.lower() for d in self.dim_files]
        ]

    def get_orphan_views(self):

        return [v for v in self.view_files if v.cube.lower() not in [c.stem for c in self.cube_files]]

    def get_orphan_subsets(self):

        return [s for s in self.sub_files if s.dimension.lower() not in [d.stem.lower() for d in self.dim_files]]

    def get_orphan_feeders(self):

        return [f for f in self.feeders_files if f.stem.lower() not in [c.stem for c in self.cube_files]]

    def _scan_all(self):

        self.dim_files = self._find_dims()
        self.cube_files = self._find_cubes()
        self.rules_files = self._find_rules()
        self.cma_files = self._find_cmas()
        self.view_files = self._find_views()
        self.sub_files = self._find_subs()
        self.feeders_files = self._find_feeders()
        self.non_tm1_files = self._find_non_tm1()
        self.process_files = self._find_processes()
        # disabling this for now, need to handle potential different path
        # self.log_files = self._find_logs()

    def _find_dims(self):
        """
        Returns a list of all dim file objects
        """

        return [TM1DimensionFile(d) for d in self._find_files(TM1DimensionFile.suffix)]

    def _find_cubes(self):

        return [TM1CubeFile(c) for c in self._find_files(TM1CubeFile.suffix)]

    def _find_rules(self):

        return [TM1RulesFile(r) for r in self._find_files(TM1RulesFile.suffix)]

    def _find_feeders(self):

        return [TM1FeedersFile(f) for f in self._find_files(TM1FeedersFile.suffix)]

    def _find_processes(self):

        return [TM1ProcessFile(f) for f in self._find_files(TM1ProcessFile.suffix)]

    def _find_subs(self):

        return [
            TM1SubsetFile(
                s,
            )
            for s in self._find_files(TM1SubsetFile.suffix, recursive=True)
        ]

    def _find_views(self):

        return [
            TM1ViewFile(
                v,
            )
            for v in self._find_files(TM1ViewFile.suffix, recursive=True)
        ]

    def _find_cmas(self):

        return [TM1CMAFile(r) for r in self._find_files(TM1CMAFile.suffix, recursive=True)]

    def _find_logs(self):
        # this needs work, need to think about how to handle separate log file
        return [TM1LogFile(log) for log in self._find_files(TM1LogFile.suffix)]

    def _find_non_tm1(self, recursive: bool = False):

        # I wasn't quite sure what functionality I wanted here but decided
        # a generic method that could be applied recursively or not to
        # a specific path might work best (although the naming is a bit confusing)
        # Using this recursively might perform poorly

        files = [NonTM1File(f) for f in self._find_files(suffix="*", recursive=recursive)]

        for f in files:
            # this will remove other random files with these suffixes
            # e.g. other random cfg files
            # so not perfect
            if f.suffix.lower() in self.suffixes:

                files.remove(f)

        return files

    def _find_files(self, suffix: str, recursive: bool = False, prefix: str = "", path: Path = None):

        if path:
            return self._case_insensitive_glob(path, f"{prefix}*.{suffix}", recursive=recursive)

        return self._case_insensitive_glob(self.data_path, f"{prefix}*.{suffix}", recursive=recursive)

    def _find_config_file(self):

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

    @staticmethod
    def _case_insensitive_glob(path: Path, pattern: str, recursive: bool = False):
        def either(c):
            return "[%s%s]" % (c.lower(), c.upper()) if c.isalpha() else c

        if recursive:
            return path.rglob("".join(map(either, pattern)))

        return path.glob("".join(map(either, pattern)))
