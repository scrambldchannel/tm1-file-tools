# simplify API in files/__init.py__ ?
from pathlib import Path, PureWindowsPath, WindowsPath

# from tm1filetools.files.base import TM1File
from tm1filetools.files import (
    NonTM1File,
    TM1AttributeCubeFile,
    TM1AttributeDimensionFile,
    TM1BLBFile,
    TM1CfgFile,
    TM1ChangeLogFile,
    TM1CMAFile,
    TM1CubeFile,
    TM1DimensionFile,
    TM1FeedersFile,
    TM1LogFile,
    TM1ProcessErorrLogFile,
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
        TM1BLBFile.suffix,
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
        self._data_path, self._log_path = self._get_paths_from_cfg()

        # scan for all file types
        # this we want to replace for performance sakes
        self._scan_all()

    def re_scan(self):

        self._scan_all()

    def delete(self, file_object):

        file_object.delete()

        self._scan_all()

    def rename(self, file_object, new_name: str):

        file_object.rename(new_name)

        self._scan_all()

    def delete_all_feeders(self):

        for fd in self._feeders_files:
            fd.delete()

        self._find_feeders()

    def delete_all_orphans(self):

        self.delete_orphan_rules()
        self.delete_orphan_attr_dims()
        self.delete_orphan_attr_cubes()
        self.delete_orphan_views()
        self.delete_orphan_subs()
        self.delete_orphan_feeders()

    def delete_all_blbs(self):

        for b in self._blb_files:
            b.delete()

        self.blb_files = self._find_blbs()

    def delete_orphan_rules(self):

        for r in self.get_orphan_rules():
            r.delete()

        self._rules_files = self._find_rules()

    def delete_orphan_attr_dims(self):

        for d in self.get_orphan_attr_dims():
            d.delete()

        self._find_dims()

    def delete_orphan_attr_cubes(self):

        for c in self.get_orphan_attr_cubes():
            c.delete()

        self._find_cubes()

    def delete_orphan_views(self):

        for v in self.get_orphan_views():
            v.delete()

        self._view_files = self._find_views()

    def delete_orphan_subs(self):

        for s in self.get_orphan_subsets():
            s.delete()

        self._sub_files = self._find_subs()

    def delete_orphan_feeders(self):

        for f in self.get_orphan_feeders():
            f.delete()

        self._find_feeders()

    def get_model_cubes(self):

        return [c for c in self._cube_files if not c.is_control]

    def get_model_dims(self):

        return [d for d in self._dim_files if not d.is_control]

    def get_control_cubes(self):

        return [c for c in self._cube_files if c.is_control]

    def get_control_dims(self):

        return [d for d in self._dim_files if d.is_control]

    def get_control_procs(self):

        return [p for p in self._proc_files if p.is_control]

    def get_control_views(self):

        return [v for v in self._view_files if v.is_control]

    def get_control_subs(self):

        return [s for s in self._sub_files if s.is_control]

    def get_attr_cubes(self):

        return [TM1AttributeCubeFile(c._path) for c in self._cube_files if c.name.find(c.attribute_prefix) == 0]

    def get_attr_dims(self):

        return [
            TM1AttributeDimensionFile(d._path)
            for d in self._dim_files
            if d.name.lower().find(d.attribute_prefix.lower()) == 0
        ]

    def get_orphan_rules(self):

        return [r for r in self._rules_files if r.stem.lower() not in [c.stem.lower() for c in self._cube_files]]

    def get_orphan_attr_dims(self):

        return [
            a for a in self.get_attr_dims() if a.strip_prefix().lower() not in [d.stem.lower() for d in self._dim_files]
        ]

    def get_orphan_attr_cubes(self):

        return [
            a
            for a in self.get_attr_cubes()
            if a.strip_prefix().lower() not in [d.stem.lower() for d in self._dim_files]
        ]

    def get_orphan_views(self):

        return [v for v in self._view_files if v.cube.lower() not in [c.stem.lower() for c in self._cube_files]]

    def get_orphan_subsets(self):

        return [s for s in self._sub_files if s.dimension.lower() not in [d.stem.lower() for d in self._dim_files]]

    def get_orphan_feeders(self):

        return [f for f in self._feeders_files if f.stem.lower() not in [c.stem.lower() for c in self._cube_files]]

    def _scan_all(self):

        self._find_dims()
        self._find_cubes()
        self._rules_files = self._find_rules()
        self._cma_files = self._find_cmas()
        self._view_files = self._find_views()
        self._sub_files = self._find_subs()
        self._find_feeders()
        self._non_tm1_files = self._find_non_tm1()
        self._proc_files = self._find_processes()
        self._log_files = self._find_logs()
        self._find_blbs()

    def _find_dims(self):
        """
        Returns a list of all dim file objects
        """

        self._dim_files = [TM1DimensionFile(d) for d in self._find_files(TM1DimensionFile.suffix)]

    def _find_cubes(self):

        self._cube_files = [TM1CubeFile(c) for c in self._find_files(TM1CubeFile.suffix)]

    def _find_rules(self):

        return [TM1RulesFile(r) for r in self._find_files(TM1RulesFile.suffix)]

    def _find_feeders(self):

        self._feeders_files = [TM1FeedersFile(f) for f in self._find_files(TM1FeedersFile.suffix)]

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

    def _find_blbs(self):
        """
        Returns a list of all blb file objects
        """

        self._blb_files = [TM1BLBFile(b) for b in self._find_files(TM1BLBFile.suffix)]

    def _find_logs(self):

        # logs may be in a different path so search with the glob func
        # We should also be careful of the tm1s.log file as we may fail to get a lock on it

        logs = []
        for log in self._case_insensitive_glob(self._log_path, f"*.{TM1LogFile.suffix}"):
            # if we think this is the tm1s.log file, use the derived class that avoids trying to open it
            if log.stem.lower() == "tm1s":
                logs.append(TM1ChangeLogFile(log))
            elif log.stem.lower().startswith(TM1ProcessErorrLogFile.prefix.lower()):
                logs.append(TM1ProcessErorrLogFile)
            else:
                logs.append(TM1LogFile(log))

        return logs

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

        return self._case_insensitive_glob(self._data_path, f"{prefix}*.{suffix}", recursive=recursive)

    def _find_config_file(self):

        cfg_file_path = next(self._case_insensitive_glob(path=self._path, pattern="tm1s.cfg"), None)

        if cfg_file_path:
            return TM1CfgFile(cfg_file_path)

        return None

    def _get_paths_from_cfg(self):

        # if we can't find a valid config file, use the init path for data and logs
        if not self.config_file:
            return self._path, self._path

        # read the params from the config file and see if a concrete path can be derived
        data_dir = self.config_file.get_parameter("DataBaseDirectory")
        log_dir = self.config_file.get_parameter("LoggingDirectory")

        return self._derive_path(data_dir), self._derive_path(log_dir)

    def _derive_path(self, dir: str):

        if dir:

            pure_path = PureWindowsPath(dir)

            if pure_path.is_absolute():

                if self._local:
                    return WindowsPath(pure_path)

                # We can't do much with an absolute path when running on a separate machine
                return self._path

            else:
                # thanks to the magic of pathlib, this seems to work cross platform :)
                # note, I've made it an absolute path, not sure this is strictly necessary
                return Path.joinpath(self._path, pure_path).resolve()

        return self._path

    @staticmethod
    def _case_insensitive_glob(path: Path, pattern: str, recursive: bool = False):
        def either(c):
            return "[%s%s]" % (c.lower(), c.upper()) if c.isalpha() else c

        if recursive:
            return path.rglob("".join(map(either, pattern)))

        return path.glob("".join(map(either, pattern)))
