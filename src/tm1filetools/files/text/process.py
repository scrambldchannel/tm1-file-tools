import json
from pathlib import Path

from .text import TM1TextFile


class TM1ProcessFile(TM1TextFile):
    """
    A class representation of a tm1 TI process file. A TM1 .pro file


    """

    suffix = "pro"

    # this might need to be localised
    delimiter = ","
    quote_character = '"'

    # line codes - see https://gist.github.com/scrambldchannel/9955cb731f80616c706f2d5a81b82c2a
    _linecode_lookup = {
        "601": {
            "Code": "601",
            "Descriptions": "version",
            "Java Api Name": "ProcessFileVersionNumber",
            "Multilines": False,
            "Multiline with keys": False,
            "Type": "Numeric",
        },
        "602": {
            "Code": "601",
            "Descriptions": "",
            "Java Api Name": "ProcessName",
            "Multilines": False,
            "Multiline with keys": False,
            "Type": "Single String",
        },
    }

    def __init__(self, path: Path):

        super().__init__(path)

        self.prolog = None
        self.metadata = None
        self.data = None
        self.epilog = None

    # Attempt some simple parsing

    # https://gist.github.com/scrambldchannel/9955cb731f80616c706f2d5a81b82c2a

    def _get_line_by_code(self, linecode: int):

        # Are lines ever duplicated?

        # just need to remember how to read a file line by line here
        for line in self.readlines():

            code = line[0:3]

            if code == str(linecode):

                line = str.join("", line[4:]).strip(self.quote_character)
                return (code, line)

    def to_json(self, sort_keys: bool = True):

        _, name = self._get_line_by_code(602)

        json_dump = {
            "Name": name,
        }

        return json.dumps(json_dump, sort_keys=sort_keys, indent=4)

    @staticmethod
    def _parse_single_int(line: str) -> int:
        """
        Read a line containing a single int and return the value only
        """

        delimiter = ","

        return int(line.split(delimiter)[1])

    @staticmethod
    def _parse_single_string(line: str) -> str:
        """
        Read a line containing a code and a single string and return the value only
        """

        delimiter = ","
        quote_character = '"'

        # This gives you the entire string with the code removed
        # it might have been easier to just strip the first four characters ;)

        return str.join("", line.split(delimiter)[1:]).strip(quote_character)
