from pathlib import Path, PureWindowsPath, WindowsPath

from tm1filetools.files import TM1CfgFile

from .base import TM1BaseFileTool


class TM1CfgFileTool(TM1BaseFileTool):
    """
    TM1 cfg file tool class

    """

    def __init__(self, path: Path, local: bool = False):

        self._path: Path = path

        self._path = path

        self._local = local

        self.config_file = self._find_config_file()

    def _find_config_file(self):

        if self._path.is_dir():
            self._path = Path.joinpath(self._path, "tm1s.cfg")

        if self._path.exists():
            return TM1CfgFile(self._path)

    def get_data_path(self):

        if self.config_file:
            if self.config_file.is_valid():
                return self._derive_path(self.config_file.get_parameter("DataBaseDirectory"))

    def get_log_path(self):

        if self.config_file:
            if self.config_file.is_valid():

                return self._derive_path(self.config_file.get_parameter("LoggingDirectory"))

    def _derive_path(self, dir: str):

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
