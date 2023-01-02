from pathlib import Path

from .linecode import (  # TM1LinecodeRowSingleInt,
    TM1LinecodeFile,
    TM1LinecodeRowSingleString,
)
from .user_owned import TM1UserFile


class TM1ViewFile(TM1UserFile, TM1LinecodeFile):
    """
    A class representation of a tm1 view file

    """

    # still can't really decide if this belongs here
    suffix = "vue"
    folder_suffix = "}vues"

    def __init__(self, path: Path, public: bool = True):

        super().__init__(path)

        # does this assumption hold true or do vue files sometimes get nested further?
        self.cube = self._get_object_name()
        self.public = public
        self.owner = self._get_owner_name()
        self.view_name = self.stem

    def _to_json(self):

        # Fields that need to be populated
        # "Name"
        # "Columns",
        # "Rows",
        # "Titles",
        # "SuppressEmptyColumns",
        # "SuppressEmptyRows",
        # "FormatString",

        name = self._get_name()
        format = self._get_format()
        rows = self._get_rows()
        cols = self._get_columns()
        titles = self._get_titles()

        empty_cols = self._get_suppress_empty_cols()
        empty_rows = self._get_suppress_empty_rows()

        return {
            "Name": name,
            "FormatString": format,
            "Rows": rows,
            "Columns": cols,
            "Titles": titles,
            "SuppressEmptyColumns": empty_cols,
            "SuppressEmptyRows": empty_rows,
        }

    def _get_name(self) -> str:

        code = 390

        return TM1LinecodeRowSingleString(self._get_line_by_code(code)).value

    def _get_format(self) -> str:

        code = 375

        # this isn't quite right, need to further parse the value
        # e.g. b:0.#########G|0| -> 0.#########
        # but I need to look in more detail

        return TM1LinecodeRowSingleString(self._get_line_by_code(code)).value

    # these need to be implemented
    def _get_columns(self) -> str:

        pass

    def _get_rows(self) -> str:

        pass

    def _get_titles(self) -> str:

        pass

    def _get_suppress_empty_cols(self) -> bool:

        # this is likely a code with a single binary int
        pass

    def _get_suppress_empty_rows(self) -> bool:

        # this is likely a code with a single binary int
        pass
