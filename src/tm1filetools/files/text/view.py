from pathlib import Path

from .linecode import TM1LinecodeFile
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
