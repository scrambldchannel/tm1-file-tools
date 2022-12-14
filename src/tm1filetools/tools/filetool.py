from pathlib import Path
from typing import List, Optional

from tm1filetools.files import (
    NonTM1File,
    TM1AttributeCubeFile,
    TM1AttributeDimensionFile,
    TM1BLBFile,
    TM1ChoreFile,
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
from tm1filetools.files.base import TM1File

from .base import TM1BaseFileTool

# from .cfgfiletool import TM1CfgFileTool
from .logfiletool import TM1LogFileTool


class TM1FileTool(TM1BaseFileTool):
    """
    TM1 file tool object

    """

    def __init__(self, path: Path, local: bool = False):

        self._path: Path = path

        # local means the code is running on the machine the folder exists
        # this means that an absolute path in the cfg file can be used
        self._local: bool = local

        # just set these to the current path
        # can be overwritten potentially if using a config file to derive separate paths
        self._data_path, self._log_path = self._path, self._path

        self.logfile_tool: TM1LogFileTool = TM1LogFileTool(self._log_path)

        # Fetch lists of files on demand

        # core model files
        self._dim_files: Optional[list] = None
        self._cube_files: Optional[list] = None
        # core code files
        self._rules_files: Optional[list] = None
        self._proc_files: Optional[list] = None
        # other model files
        self._sub_files: Optional[list] = None
        self._view_files: Optional[list] = None
        self._feeders_files: Optional[list] = None
        self._chore_files: Optional[list] = None
        # logs
        self._log_files: Optional[list] = None
        # other cruft
        self._cma_files: Optional[list] = None
        self._blb_files: Optional[list] = None
        self._non_tm1_files: Optional[list] = None

    def find_all(self):
        """
        Do a full scan of the dir(s) and populate all lists of files
        """

        self._find_dims()
        self._find_cubes()
        self._find_rules()
        self._find_procs()
        self._find_subs()
        self._find_views()
        self._find_feeders()
        self.logfile_tool._find_logs()
        self._find_cmas()
        self._find_blbs()
        self._find_chores()
        self._find_non_tm1()

    # getters for all file types

    def get_dims(self, model: bool = True, control: bool = False) -> List[TM1DimensionFile]:
        """Returns list of all dimension files

        Args:
            model: Return model dims (i.e. not prefixed with "}")
            control: Return control dims (i.e. prefixed with "}")

        Returns:
            List of dimension files
        """
        if self._dim_files is None:
            self._find_dims()

        return self._filter_model_and_or_control(self._dim_files, model=model, control=control)

    def get_cubes(self, model: bool = True, control: bool = False) -> List[TM1CubeFile]:
        """Returns list of all cube files

        Args:
            model: Return model cubes (i.e. not prefixed with "}")
            control: Return control cubes (i.e. prefixed with "}")

        Returns:
            List of cube files
        """

        if self._cube_files is None:
            self._find_cubes()

        return self._filter_model_and_or_control(self._cube_files, model=model, control=control)

    def get_rules(self, model: bool = True, control: bool = False) -> List[TM1RulesFile]:
        """Returns list of all cube rules files

        Args:
            model: Return model cube rules (i.e. not prefixed with "}")
            control: Return control cube rules (i.e. prefixed with "}")

        Returns:
            List of cube rules files
        """

        if self._rules_files is None:
            self._find_rules()

        return self._filter_model_and_or_control(self._rules_files, model=model, control=control)

    def get_procs(self, model: bool = True, control: bool = False) -> List[TM1ProcessFile]:
        """Returns list of all TI process files

        Args:
            model: Return model procs (i.e. not prefixed with "}")
            control: Return control procs (i.e. prefixed with "}")

        Returns:
            List of proc files
        """

        if self._proc_files is None:
            self._find_procs()

        return self._filter_model_and_or_control(self._proc_files, model=model, control=control)

    def get_subs(self, model: bool = True, control: bool = False) -> List[TM1SubsetFile]:
        """Returns list of all dimension subset files

        Args:
            model: Return model subsets (i.e. not prefixed with "}")
            control: Return control subsets (i.e. prefixed with "}")

        Returns:
            List of subset files
        """

        if self._sub_files is None:
            self._find_subs()

        return self._filter_model_and_or_control(self._sub_files, model=model, control=control)

    def get_views(self, model: bool = True, control: bool = False) -> List[TM1ViewFile]:
        """Returns list of all cube view files

        Args:
            model: Return model cube views (i.e. not prefixed with "}")
            control: Return control cube views (i.e. prefixed with "}")

        Returns:
            List of cube view files
        """

        if self._view_files is None:
            self._find_views()

        return self._filter_model_and_or_control(self._view_files, model=model, control=control)

    def get_feeders(self, model: bool = True, control: bool = False) -> List[TM1FeedersFile]:
        """Returns list of all cube feeder files

        Args:
            model: Return model cube feeders (i.e. not prefixed with "}")
            control: Return control cube feeders (i.e. prefixed with "}")

        Returns:
            List of cube feeder files
        """

        if self._feeders_files is None:
            self._find_feeders()

        return self._filter_model_and_or_control(self._feeders_files, model=model, control=control)

    def get_chores(self, model: bool = True, control: bool = False) -> List[TM1ChoreFile]:
        """Returns list of all chore files

        Args:
            model: Return model chores (i.e. not prefixed with "}")
            control: Return control chores (i.e. prefixed with "}")

        Returns:
            List of chore files
        """

        if self._chore_files is None:
            self._find_chores()

        return self._filter_model_and_or_control(self._chore_files, model=model, control=control)

    def get_blbs(self, model: bool = True, control: bool = False) -> List[TM1BLBFile]:
        """Returns list of all blb files

        Args:
            model: Return model blbs (i.e. not prefixed with "}")
            control: Return control blbs (i.e. prefixed with "}")

        Returns:
            List of blb files
        """

        if self._blb_files is None:
            self._find_blbs()

        return self._filter_model_and_or_control(self._blb_files, model=model, control=control)

    def get_cmas(self) -> List[TM1CMAFile]:
        """Returns list of all cma files

        Returns:
            List of cma files
        """

        if self._cma_files is None:
            self._find_cmas()

        return self._cma_files

    # specific control object getters

    def get_attr_dims(self) -> List[TM1AttributeDimensionFile]:
        """Returns list of all attribute dim files

        Returns:
            List of attribute dim files
        """

        return [
            TM1AttributeDimensionFile(d._path)
            for d in self.get_dims(control=True)
            if d.name.lower().find(d.attribute_prefix.lower()) == 0
        ]

    def get_attr_cubes(self) -> List[TM1AttributeCubeFile]:
        """Returns list of all attribute cube files

        Returns:
            List of attribute cube files
        """

        return [
            TM1AttributeCubeFile(c._path) for c in self.get_cubes(control=True) if c.name.find(c.attribute_prefix) == 0
        ]

    # orphan getters

    def get_orphan_rules(self) -> List[TM1RulesFile]:
        """Returns list of rules files that don't have corresponding cube files

        Returns:
            List of rules files
        """

        return [r for r in self.get_rules() if r.stem.lower() not in [c.stem.lower() for c in self.get_cubes()]]

    def get_orphan_attr_dims(self) -> List[TM1DimensionFile]:
        """Returns list of attribute dim files that don't have corresponding dim files

        Returns:
            List of dim files
        """

        return [
            a for a in self.get_attr_dims() if a.strip_prefix().lower() not in [d.stem.lower() for d in self.get_dims()]
        ]

    def get_orphan_attr_cubes(self) -> List[TM1CubeFile]:
        """Returns list of attribute cube files that don't have corresponding dim files

        Returns:
            List of cube files
        """

        return [
            a
            for a in self.get_attr_cubes()
            if a.strip_prefix().lower() not in [d.stem.lower() for d in self.get_dims(control=True)]
        ]

    def get_orphan_subs(self) -> List[TM1SubsetFile]:
        """Returns list of subset files that don't have corresponding dim files

        Returns:
            List of subset files
        """

        return [
            s
            for s in self.get_subs(control=True)
            if s.dimension.lower() not in [d.stem.lower() for d in self.get_dims(control=True)]
        ]

    def get_orphan_views(self) -> List[TM1ViewFile]:
        """Returns list of view files that don't have corresponding cube files

        Returns:
            List of view files
        """

        return [
            v
            for v in self.get_views(control=True)
            if v.cube.lower() not in [c.stem.lower() for c in self.get_cubes(control=True)]
        ]

    def get_orphan_feeders(self) -> List[TM1FeedersFile]:
        """Returns list of feeder files that don't have corresponding cube files

        Returns:
            List of feeder files
        """

        return [
            f
            for f in self.get_feeders(control=True)
            if f.stem.lower() not in [c.stem.lower() for c in self.get_cubes(control=True)]
        ]

    # to deprecate

    def get_logs(self) -> List[TM1LogFile]:
        """Returns list of all log files

        Returns:
            List of log files
        """

        # add deprecation warning

        if self._log_files is None:
            self.logfile_tool._find_logs()

        return self._log_files

    # generic operations on objects

    def delete(self, file_object: TM1File) -> int:
        """Deletes the file specified and updates properties of the file tool object

        Args:
            file_object: Instance of a file object to delete

        """

        count = file_object.delete()

        # potentially slow
        # This is all a bit hacky because the delete method in the object itself
        # Doesn't know anything about the file tool object
        self.find_all()

        return count

    def rename(self, file_object, new_name: str) -> None:
        """Renames the file specified and updates properties of the file tool object

        Args:
            file_object: Instance of a file object to rename
            new_name: New name for stem of file object
        """

        file_object.rename(new_name)

        # potentially slow
        self.find_all()

    # bulk deletes for relevant objects

    def delete_all_feeders(self) -> int:
        """Deletes all currently found feeder files

        Returns:
            int: count of files deleted
        """

        count = 0
        for fd in self.get_feeders():
            count = count + fd.delete()

        self._find_feeders()

        return count

    def delete_all_blbs(self) -> int:
        """Deletes all currently found blb files

        Returns:
            int: count of files deleted
        """

        count = 0
        for b in self.get_blbs(control=True):
            count = count + b.delete()

        self._find_blbs()

        return count

    # bulk deletes for orphans

    def delete_all_orphans(self) -> int:
        """Deletes all orphan files (rules, attribute dims etc)

        Returns:
            int: count of files deleted

        """

        count = 0
        count = count + self.delete_orphan_rules()
        count = count + self.delete_orphan_attr_dims()
        count = count + self.delete_orphan_attr_cubes()
        count = count + self.delete_orphan_views()
        count = count + self.delete_orphan_subs()
        count = count + self.delete_orphan_feeders()

        # should we rescan here?
        return count

    def delete_orphan_rules(self) -> int:
        """Deletes all orphan rules files

        Returns:
            int: count of files deleted
        """

        count = 0
        for r in self.get_orphan_rules():
            count = count + r.delete()

        self._find_rules()

        return count

    def delete_orphan_attr_dims(self) -> int:
        """Deletes all orphan attribute dim files

        Returns:
            int: count of files deleted
        """

        count = 0
        for d in self.get_orphan_attr_dims():
            count = count + d.delete()

        self._find_dims()

        return count

    def delete_orphan_attr_cubes(self) -> int:
        """Deletes all orphan attribute cube files

        Returns:
            int: Count of files deleted
        """

        count = 0
        for c in self.get_orphan_attr_cubes():
            c.delete()

        self._find_cubes()

        return count

    def delete_orphan_views(self) -> int:
        """Deletes all orphan attribute view files

        Returns:
            int: count of files deleted
        """

        count = 0
        for v in self.get_orphan_views():
            count = count + v.delete()

        self._find_views()

        return count

    def delete_orphan_subs(self) -> int:
        """Deletes all orphan attribute subset files

        Returns:
            int: count of files deleted

        """

        count = 0
        for s in self.get_orphan_subs():
            count = count + s.delete()

        self._find_subs()

        return count

    def delete_orphan_feeders(self) -> int:
        """Deletes all orphan feeder files
        Returns:
            int: count of files deleted
        """

        count = 0
        for f in self.get_orphan_feeders():
            count = count + f.delete()

        self._find_feeders()

        return count

    # finders for different file types

    def _find_dims(self):
        """
        Returns a list of all dim file objects
        """

        self._dim_files = [TM1DimensionFile(d) for d in self._find_files(TM1DimensionFile.suffix)]

    def _find_cubes(self):

        self._cube_files = [TM1CubeFile(c) for c in self._find_files(TM1CubeFile.suffix)]

    def _find_rules(self):

        self._rules_files = [TM1RulesFile(r) for r in self._find_files(TM1RulesFile.suffix)]

    def _find_procs(self):

        self._proc_files = [TM1ProcessFile(f) for f in self._find_files(TM1ProcessFile.suffix)]

    def _find_subs(self):

        self._sub_files = [
            TM1SubsetFile(
                s,
            )
            for s in self._find_files(TM1SubsetFile.suffix, recursive=True)
        ]

    def _find_views(self):

        self._view_files = [
            TM1ViewFile(
                v,
            )
            for v in self._find_files(TM1ViewFile.suffix, recursive=True)
        ]

    def _find_feeders(self):

        self._feeders_files = [TM1FeedersFile(f) for f in self._find_files(TM1FeedersFile.suffix)]

    def _find_chores(self):

        self._chore_files = [TM1ChoreFile(f) for f in self._find_files(TM1ChoreFile.suffix)]

    def _find_cmas(self):

        self._cma_files = [TM1CMAFile(r) for r in self._find_files(TM1CMAFile.suffix, recursive=True)]

    def _find_blbs(self):
        """
        Returns a list of all blb file objects
        """

        self._blb_files = [TM1BLBFile(b) for b in self._find_files(TM1BLBFile.suffix)]

    def _find_non_tm1(self, recursive: bool = False):

        # I wasn't quite sure what functionality I wanted here but decided
        # a generic method that could be applied recursively or not to
        # a specific path might work best (although the naming is a bit confusing)
        # Using this recursively might perform poorly

        files = [NonTM1File(f) for f in self._find_files(suffix="*", recursive=recursive)]

        non_tm1 = [f for f in files if f.suffix.lower() not in self.suffixes]

        self._non_tm1_files = non_tm1

    def _find_files(self, suffix: str, recursive: bool = False, prefix: str = "", path: Path = None):

        if path:
            return self._case_insensitive_glob(path, f"{prefix}*.{suffix}", recursive=recursive)

        return self._case_insensitive_glob(self._data_path, f"{prefix}*.{suffix}", recursive=recursive)

    @staticmethod
    def _filter_model_and_or_control(objects, model: bool = True, control: bool = False):

        if model and control:
            return objects

        if model:
            return [o for o in objects if not o.is_control]

        if control:
            return [o for o in objects if o.is_control]
