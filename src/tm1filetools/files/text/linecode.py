import itertools
from pathlib import Path

from .text import TM1TextFile


class TM1LinecodeRowBase:

    """Representation of a single line in the line code file log"""

    # think this constant
    _code_delimiter = ","
    _code_quote = '"'

    def __init__(self, row: str):

        self._row = row

    @classmethod
    def parse_single_int(cls, line: str) -> int:
        """
        Read a line with a code and a single int value and return the value only
        """

        _, value = line.split(cls._code_delimiter)

        # in some cases, we may have nothing there, rather than a 0
        # e.g. the mdx line of a static subset

        if value:
            return int(value)
        else:
            return 0

    @classmethod
    def parse_single_string(cls, line: str) -> str:
        """
        Read a value string containing a single string and return the value without quotes
        """

        chunks = line.split(cls._code_delimiter)

        value = str.join(",", chunks[1:])

        # hack for getting the delimiter - will need to be done better
        if value == '""""':
            return '"'

        return value.strip(cls._code_quote)

    @classmethod
    def parse_key_value_pair_string(cls, line: str):

        # e.g. 'pPeriod,"All"'

        key = line.split(cls._code_delimiter)[0]
        value = str.join("", line.split(cls._code_delimiter)[1:]).strip(cls._code_quote)

        return key, value

    @classmethod
    def parse_key_value_pair_int(cls, line: str):

        # e.g. 'pLogging,0'

        key = line.split(cls._code_delimiter)[0]
        value = int(line.split(cls._code_delimiter)[1])

        return key, value


class TM1LinecodeRowSingleInt(TM1LinecodeRowBase):

    """Representation of a single line in the line code file log"""

    def __init__(self, row: str):

        super().__init__(row)

        self.value: int = self.parse_single_int(row)


class TM1LinecodeRowSingleString(TM1LinecodeRowBase):

    """Representation of a single line in the line code file log"""

    def __init__(self, row: str):

        super().__init__(row)

        self.value: int = self.parse_single_string(row)


class TM1LinecodeRowKeyValueString(TM1LinecodeRowBase):

    """Representation of a single line in the line code file log"""

    def __init__(self, row: str):

        super().__init__(row)

        self.key, self.value = self.parse_key_value_pair_string(row)


class TM1LinecodeRowKeyValueInt(TM1LinecodeRowBase):

    """Representation of a single line in the line code file log"""

    def __init__(self, row: str):

        super().__init__(row)

        self.key, self.value = self.parse_key_value_pair_int(row)


# Can perhaps make these abstract classes
class TM1LinecodeFile(TM1TextFile):
    """
    Class with extra methods for dealing with files that are plain text but use line numbers to specify things

    Examples are subsets, views, processes and chores (I think)

    """

    _code_delimiter = ","

    # A couple more constants that simply writing special chars to json
    single_quote_json = "'"
    double_quote_json = '"'

    def __init__(self, path: Path):

        super().__init__(path)

    def reader(self, linecode=None, start_offset=0, end_offset=1):

        # the idea here is to have a generic generator that returns a row obj for each line

        with open(self._path, "r") as f:
            for row in f:

                yield TM1LinecodeRowBase(row)

    def _get_lines_by_index(self, index: int, line_count: int = 1, rstrip=True):

        with open(self._path, "r") as f:
            lines = itertools.islice(f, index, index + line_count)

            if rstrip:
                return [line.rstrip() for line in lines]
            else:

                return list(lines)

    def _get_lines_by_code(self, linecode: int, rstrip=True):
        """
        Return a list of lines in a file for the specific code
        """

        lines = []

        with open(self._path, "r") as f:

            for line in f:

                code = line.split(self._code_delimiter)[0]

                if code == str(linecode):
                    if rstrip:
                        lines.append(line.rstrip())
                    else:
                        lines.append(line)

        return lines

    def _get_line_by_code(self, linecode: int, rstrip=True):

        # only useful where a single line expected
        return self._get_lines_by_code(linecode=linecode, rstrip=rstrip)[0]

    def _get_int_val_by_code(self, linecode: int):

        row = TM1LinecodeRowSingleInt(self._get_lines_by_code(linecode=linecode)[0])

        return row.value

    def _get_str_val_by_code(self, linecode: int):

        row = TM1LinecodeRowSingleString(self._get_lines_by_code(linecode=linecode)[0])

        return row.value

    def _get_str_key_val_by_code(self, linecode: int):

        row = TM1LinecodeRowKeyValueString(self._get_lines_by_code(linecode=linecode)[0])

        return row.value

    def _get_indexes_by_code(self, linecode: int):

        # Are lines ever duplicated?
        # Yes, they are. E.g. in view files, code 7 and 270
        # seem like they appear once for every

        with open(self._path, "r") as f:

            indexes = []

            for index, line in enumerate(f):

                code = line.split(self._code_delimiter)[0]

                if code == str(linecode):
                    indexes.append(index)

        return indexes

    def _get_index_by_code(self, linecode: int):

        # hack to maintain backwards compatibility
        # only use where codes exist only once

        return self._get_indexes_by_code(linecode=linecode)[0]

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
        index = self._get_index_by_code(linecode)
        line = self._get_line_by_code(linecode)

        # parse the line to get the number of lines
        # hack
        row = TM1LinecodeRowSingleInt(line)

        lines = self._get_lines_by_index(index=index + 1, line_count=row.value, rstrip=rstrip)

        return lines
