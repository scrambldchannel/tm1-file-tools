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

    # three line auto generated code where code tabs are empty
    empty_code_tab = """
    #****Begin: Generated Statements***
    #****End: Generated Statements****
    """

    def __init__(self, path: Path):

        super().__init__(path)

        self.prolog = None
        self.metadata = None
        self.data = None
        self.epilog = None

        # Attempt some simple parsing
        # https://gist.github.com/scrambldchannel/9955cb731f80616c706f2d5a81b82c2a

    def _get_prolog_codeblock(self, to_json: bool = False):

        linecode = 572

        if to_json:
            return self._codeblock_to_json_str(self._get_multiline_block(linecode))

        return self._get_multiline_block(linecode)

    def _get_metadata_codeblock(self, to_json: bool = False):

        linecode = 573

        return self._get_multiline_block(linecode)

    def _get_data_codeblock(self, to_json: bool = False):

        linecode = 574

        return self._get_multiline_block(linecode)

    def _get_epilog_codeblock(self, to_json: bool = False):

        linecode = 575

        return self._get_multiline_block(linecode)

    def _get_line_by_code(self, linecode: int):

        # Are lines ever duplicated?
        lines = self.readlines()

        for index, line in enumerate(lines):

            code = line[0:3]

            if code == str(linecode):
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

        # janky
        value = self._parse_single_int(value)

        lines = []

        for i in range(index + 1, index + value + 1):

            line = self._get_line_by_index(i)
            lines.append(line)

        if value == len(lines):
            lines_correct = True
        else:
            lines_correct = False

        return value, lines, lines_correct

    @staticmethod
    def _codeline_strip_whitespace(line: str) -> str:
        return line.rstrip()

    @staticmethod
    def _codeblock_to_json_str(lines: list[str]) -> str:

        # how portable is this?
        newline = "\r\n"

        json_str: str = ""
        for line in lines:
            json_str = json_str + line + newline

        return json_str.removesuffix(newline)
