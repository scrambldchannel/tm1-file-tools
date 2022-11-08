from pathlib import Path

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
