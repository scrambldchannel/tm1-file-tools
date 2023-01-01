from pathlib import Path
from typing import Optional

from .linecode import (
    TM1LinecodeFile,
    TM1LinecodeRowSingleInt,
    TM1LinecodeRowSingleString,
)
from .user_owned import TM1UserFile


class TM1SubsetFile(TM1UserFile, TM1LinecodeFile):
    """
    A class representation of a tm1 subset file

    """

    suffix = "sub"
    folder_suffix = "}subs"

    def __init__(self, path: Path, public: bool = True):

        super().__init__(path)

        self.dimension = self._get_object_name()
        self.public = public
        self.owner = self._get_owner_name()
        # subset_name maybe a clearer API than stem?
        self.subset_name = self.stem

    def is_dynamic(self) -> bool:

        return True if self._get_mdx() else False

    def _get_mdx(self) -> Optional[str]:
        """Read file and return the MDX, if file defines a dynamic subset, or None

        Returns:
            A string containing the MDX or None

        """

        # this is captured by key 275
        code = 275

        mdx_chars = TM1LinecodeRowSingleInt(self._get_line_by_code(code)).value

        if mdx_chars > 0:

            mdx_idx = self._get_index_by_code(code)

            # I believe it's all on one line, not sure
            return self._get_lines_by_index(index=mdx_idx + 1)[0]

        # does this code exist in a static file? Or is it just empty?
        return None

    def _get_name(self):

        code = 284

        return TM1LinecodeRowSingleString(self._get_line_by_code(code)).value

    def _to_json(self):
        """Read file and return a json representation

        Returns:
            A dict containing a json representation of the subset

        """

        json_dump = {}

        name = self._get_name()

        json_dump["Name"] = name

        # if the file contains an mdx expression, add it
        if self._get_mdx():
            json_dump["Expression"] = self._get_mdx()

        return json_dump

    @staticmethod
    def _create_odata_string(dim: str, hier: str = None):

        # this is a fairly trivial function but may be useful more generally
        # perhaps it should be moved to a helper class?

        # derive "Hierarchy@odata.bind" string
        # Example - "Dimensions('}Processes')/Hierarchies('}Processes')"

        # use default hierarchy if none provided

        if hier is None:
            hier = dim

        return f"Dimensions('{dim}')/Hierarchies('{hier}')"
