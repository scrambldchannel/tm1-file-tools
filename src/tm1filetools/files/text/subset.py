from pathlib import Path
from typing import Optional

from .linecode import TM1LinecodeFile
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

    def _get_mdx(self) -> Optional[str]:
        """Read file and return the MDX, if file defines a dynamic subset, or None

        Returns:
            A string containing the MDX or None

        """

        mdx_idx = self._get_line_index_by_code(275) + 1

        return self._get_line_by_index(mdx_idx)
