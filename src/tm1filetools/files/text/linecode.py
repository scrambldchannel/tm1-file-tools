from pathlib import Path

from .text import TM1TextFile


# Can perhaps make these abstract classes
class TM1LinecodeFile(TM1TextFile):
    """
    Class with extra methods for dealining with files that are plain text but use line numbers to specify things

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

    def _get_line_by_index(self, index: int):

        lines = self.readlines()

        return lines[index]

    def _get_line_by_code(self, linecode: int):

        # Are lines ever duplicated?
        lines = self.readlines()

        for line in lines:

            code = line.split(self.code_delimiter)[0]

            if code == str(linecode):
                return line

    def _get_line_index_by_code(self, linecode: int):

        # Are lines ever duplicated?
        lines = self.readlines()

        for index, line in enumerate(lines):

            code = line.split(self.code_delimiter)[0]

            if code == str(linecode):
                return index

    def _parse_single_int(self, line: str) -> int:
        """
        Read a line with a code and a single int value and return the value only
        """

        _, value = line.split(self.code_delimiter)

        return int(value)

    def _parse_single_string(self, line: str) -> str:
        """
        Read a value string containing a single string and return the value without quotes
        """

        # need to make this portable

        chunks = line.split(self.code_delimiter)

        value = str.join(",", chunks[1:])

        # hack for getting the delimiter - will need to be done better
        if value == '""""':
            return '"'

        return value.strip(self.code_quote)
