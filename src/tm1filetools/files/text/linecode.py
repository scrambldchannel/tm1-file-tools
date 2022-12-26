import itertools
from pathlib import Path

from .text import TM1TextFile


# Can perhaps make these abstract classes
class TM1LinecodeFile(TM1TextFile):
    """
    Class with extra methods for dealing with files that are plain text but use line numbers to specify things

    Examples are subsets, views, processes and chores (I think)

    """

    # That is the separator used in lines, not say the datasource
    # I think it's always a comma but need to check
    code_delimiter = ","

    # likewise, I think the strings in the code itself are always delimited by double quotes
    code_quote = '"'

    # A couple more constants that simply writing special chars to json
    single_quote_json = "'"
    double_quote_json = '"'

    def __init__(self, path: Path):

        super().__init__(path)

    def _get_line_by_index(self, index: int, strip_newline=True):

        return next(itertools.islice(self.reader(strip_newline=strip_newline), index, index + 1))

    def _get_line_by_code(self, linecode: int, strip_newline=True):

        # Are lines ever duplicated?
        lines = self.reader(strip_newline=strip_newline)

        for line in lines:

            code = line.split(self.code_delimiter)[0]

            if code == str(linecode):
                return line

    def _get_line_index_by_code(self, linecode: int):

        # Are lines ever duplicated?
        lines = self.reader()

        for index, line in enumerate(lines):

            code = line.split(self.code_delimiter)[0]

            if code == str(linecode):
                return index

    @classmethod
    def _parse_single_int(cls, line: str) -> int:
        """
        Read a line with a code and a single int value and return the value only
        """

        _, value = line.split(cls.code_delimiter)

        # in some cases, we may have nothing there, rather than a 0
        # e.g. the mdx line of a static subset

        if value:
            return int(value)
        else:
            return 0

    @classmethod
    def _parse_single_string(cls, line: str) -> str:
        """
        Read a value string containing a single string and return the value without quotes
        """

        chunks = line.split(cls.code_delimiter)

        value = str.join(",", chunks[1:])

        # hack for getting the delimiter - will need to be done better
        if value == '""""':
            return '"'

        return value.strip(cls.code_quote)

    @classmethod
    def _get_key_value_pair_string(cls, line: str):

        # e.g. 'pPeriod,"All"'

        key = line.split(cls.code_delimiter)[0]
        value = str.join("", line.split(cls.code_delimiter)[1:]).strip(cls.code_quote)

        return {"key": key, "value": value}

    @classmethod
    def _get_key_value_pair_int(cls, line: str):

        # e.g. 'pLogging,0'

        key = line.split(cls.code_delimiter)[0]
        value = int(line.split(cls.code_delimiter)[1])

        return {"key": key, "value": value}

    def _get_multiline_block(self, linecode: int, rstrip: bool = True):
        """
        Read the int value from the submitted line and return the following n lines

        e.g. sensible values are:
        - 560 (ProcessParametersNames)
        - 572 (ProcessPrologProcedure)
        - 575 (ProcessEpilogProcedure)
        - etc ...

        See [gist](https://gist.github.com/scrambldchannel/9955cb731f80616c706f2d5a81b82c2a)

        """

        # get the index and the line for this code
        index = self._get_line_index_by_code(linecode)
        line = self._get_line_by_code(linecode)

        # parse the line to get the number of lines
        number_of_lines = self._parse_single_int(line)

        # This isn't the most elegant but the size of these chunks is unlikely to be large
        lines = []

        # loop over the next n lines
        index = index + 1
        for i in range(index, index + number_of_lines):

            line = self._get_line_by_index(i, strip_newline=False)
            lines.append(line)

        if rstrip:
            return [line.rstrip() for line in lines]

        return lines
