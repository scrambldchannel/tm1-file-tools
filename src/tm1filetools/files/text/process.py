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
        lines = self.readlines()

        for index, line in enumerate(lines):

            code = line[0:3]

            if code == str(linecode):
                print(line)
                value = str.join("", line[4:]).strip(self.quote_character)
                return (line, code, value, index)

    def _get_line_by_index(self, index: int):

        lines = self.readlines()

        return lines[index]

    def to_json(self, sort_keys: bool = True):

        line, _, name, _ = self._get_line_by_code(602)

        json_dump = {
            "Name": name,
        }

        return json.dumps(json_dump, sort_keys=sort_keys, indent=4)

    @staticmethod
    def _parse_single_int(value: str) -> int:
        """
        Read a value string containing a single int and return the value only
        """

        # kind of a pointless
        return int(value)

    @staticmethod
    def _parse_single_string(value: str, quote_character: str) -> str:
        """
        Read a value string containing a single string and return the value without quotes
        """

        # need to make this portable

        return value.strip(quote_character)

    def _get_multiline_block(self, linecode):
        """
        Read the int value from the submitted line and return the following n lines

        e.g. sensible values are:
        - 560 (ProcessParametersNames)
        - 572 (ProcessPrologProcedure)
        - 575 (ProcessEpilogProcedure)
        - etc ...

        See [gist](https://gist.github.com/scrambldchannel/9955cb731f80616c706f2d5a81b82c2a)

        """

        line, _, value, index = self._get_line_by_code(linecode)

        lines = []
        for i in range(index, index + int(value)):

            line = self._get_line_by_index(i)
            lines.append(line)

        # here it would be interesting to know if the correct number of lines were found
        lines_correct = value = len(lines) + 1

        return value, lines, lines_correct
