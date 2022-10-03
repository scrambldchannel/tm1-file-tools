import configparser
from pathlib import Path

from .text import TM1TextFile


class TM1CfgFile(TM1TextFile):
    """
    A class representation of a tm1.cfg file

    """

    # Could add a list of valid options here

    _section = "TM1S"

    def __init__(self, path: Path):

        super().__init__(path)

        self.config = configparser.ConfigParser()
        self.config.read(path)

    def get_parameter(self, param: str) -> str:

        return self.config.get(section=self._section, option=param, fallback=None)

    def set_parameter(self, param: str, value: str) -> None:

        # if we have a list of valid options, we could warn when an invalid option set
        # do I need to care about the section in this file?
        self.config[self._section][param] = value

        with open(self._path, "w") as f:
            self.config.write(f)
