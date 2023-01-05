from pathlib import Path

from tm1filetools.files import NonTM1File  # noqa
from tm1filetools.files import TM1AttributeCubeFile  # noqa
from tm1filetools.files import TM1AttributeDimensionFile  # noqa
from tm1filetools.files import TM1ChangeLogFile  # noqa
from tm1filetools.files import TM1LogFile  # noqa
from tm1filetools.files import TM1ProcessErorrLogFile  # noqa
from tm1filetools.files import (
    TM1BLBFile,
    TM1CfgFile,
    TM1ChoreFile,
    TM1CMAFile,
    TM1CubeFile,
    TM1DimensionFile,
    TM1FeedersFile,
    TM1ProcessFile,
    TM1RulesFile,
    TM1SubsetFile,
    TM1ViewFile,
)


class TM1BaseFileTool:
    """
    TM1 log file tool class

    """

    # populate with empty string so that we can try adding
    # a basic generator to search for files
    suffix = ""

    suffixes = [
        TM1BLBFile.suffix,
        TM1CfgFile.suffix,
        TM1CubeFile.suffix,
        TM1DimensionFile.suffix,
        TM1ProcessFile.suffix,
        TM1ChoreFile.suffix,
        TM1RulesFile.suffix,
        TM1SubsetFile.suffix,
        TM1ViewFile.suffix,
        TM1CMAFile.suffix,
        TM1FeedersFile.suffix,
    ]

    def __init__(self):

        self._path: Path = None

    def _files(self, model=True, control=False):
        """
        A generator that returns all files with the desired extension and filtering
        """

        for f in self._case_insensitive_glob(self._path, f"*.{self.suffix}"):

            is_control = f.stem.startswith("}")

            if not model and not is_control:
                continue

            if not control and is_control:
                continue

            yield f

    @staticmethod
    def _case_insensitive_glob(path: Path, pattern: str, recursive: bool = False):
        def either(c):
            return "[%s%s]" % (c.lower(), c.upper()) if c.isalpha() else c

        if recursive:
            return path.rglob("".join(map(either, pattern)))

        return path.glob("".join(map(either, pattern)))
