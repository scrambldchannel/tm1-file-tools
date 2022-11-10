from pathlib import Path, PureWindowsPath, WindowsPath

from tm1filetools.files import TM1CfgFile

from .base import TM1BaseFileTool


class TM1CfgFileTool(TM1BaseFileTool):
    """
    TM1 cfg file tool class

    """

    def __init__(self, path: Path, local: bool = False):

        self._path: Path = path

        self._path_cfg = None

        self._local: bool = local

        self.config_file: TM1CfgFile = self._find_config_file()

    def _find_config_file(self):

        if self._path.is_dir():
            self._path_cfg = Path.joinpath(self._path, "tm1s.cfg")
        else:
            self._path_cfg = self._path

        if self._path_cfg.exists():
            return TM1CfgFile(self._path_cfg)

    def _get_data_path_param(self):

        if self.config_file:
            return self.config_file.get_data_path()

    def _get_log_path_param(self):

        if self.config_file:
            return self.config_file.get_log_path()

    def _derive_path(self, path: str):

        # this method needs love, or at least commentary
        # I was trying to derive an absolute path if possible
        # from the params in the cfg file
        # but I can't quite remember what the exact behaviour
        # was supposed to be, even though I only wrote it two weeks ago!

        pure_path = PureWindowsPath(path)

        if pure_path.is_absolute():

            if self._local:
                return WindowsPath(pure_path)

            # We can't do much with an absolute path when running on a separate machine
            return self._path

        else:
            # thanks to the magic of pathlib, this seems to work cross platform :)
            # note, I've made it an absolute path, not sure this is strictly necessary
            return Path.joinpath(self._path, pure_path).resolve()

    def get_data_path(self) -> Path:

        path_str = self._get_data_path_param()

        if path_str:
            return self._derive_path(path_str)

    def get_log_path(self) -> Path:

        path_str = self._get_log_path_param()

        if path_str:
            return self._derive_path(path_str)
