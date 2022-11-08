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
    _code_block_prefix_lines = ["", "#****Begin: Generated Statements***", "#****End: Generated Statements****"]

    _datasource_type_mapping = {"CHARACTERDELIMITED": "ASCII"}

    _type_mapping = {1: "Numeric", 2: "String"}

    def __init__(self, path: Path):

        super().__init__(path)

    def _get_prolog_codeblock(self):

        linecode = 572

        return self._get_multiline_block(linecode)

    def _get_metadata_codeblock(self):

        linecode = 573

        return self._get_multiline_block(linecode)

    def _get_data_codeblock(self):

        linecode = 574

        return self._get_multiline_block(linecode)

    def _get_epilog_codeblock(self):

        linecode = 575

        return self._get_multiline_block(linecode)

    def _get_line_by_code(self, linecode: int):

        # Are lines ever duplicated?
        lines = self.readlines()

        for line in lines:

            code = line.split(self.delimiter)[0]

            if code == str(linecode):
                return line

    def _get_line_index_by_code(self, linecode: int):

        # Are lines ever duplicated?
        lines = self.readlines()

        for index, line in enumerate(lines):

            code = line.split(self.delimiter)[0]

            if code == str(linecode):
                return index

    def _get_line_by_index(self, index: int):

        lines = self.readlines()

        return lines[index]

    def to_json(self, sort_keys: bool = True):

        name = self._parse_single_string(self._get_line_by_code(602))

        prolog = self._codeblock_to_json_str(self._get_prolog_codeblock())
        metadata = self._codeblock_to_json_str(self._get_metadata_codeblock())
        data = self._codeblock_to_json_str(self._get_data_codeblock())
        epilog = self._codeblock_to_json_str(self._get_epilog_codeblock())

        security_access = self._parse_single_int(self._get_line_by_code(1217))
        security_access = security_access == 1

        parameters = self._get_parameters()
        variables = self._get_variables()

        json_dump = {
            "Name": name,
            "PrologProcedure": prolog,
            "MetadataProcedure": metadata,
            "DataProcedure": data,
            "EpilogProcedure": epilog,
            "HasSecurityAccess": security_access,
            "Parameters": parameters,
            "Variables": variables,
        }

        return json.dumps(json_dump, sort_keys=sort_keys, indent=4)

    def _get_parameters(self) -> list:

        # What does the json look like with no params?
        params = []

        # param names are from 560
        # param datatypes are from 561
        # param default values are from 590
        # param hints are from 637

        # this needs to be refactored
        idx_datatype = self._get_line_index_by_code(561)
        idx_default = self._get_line_index_by_code(590)
        idx_hint = self._get_line_index_by_code(637)

        names = self._get_multiline_block(linecode=560)

        for idx, name in enumerate(names):

            # these are single ints on the line
            datatype = self._type_mapping[int(self._get_line_by_index(idx_datatype + idx + 1))]

            hint = self._get_key_value_pair_string(self._get_line_by_index(idx_hint + idx + 1))["value"]

            default = self._get_key_value_pair_string(self._get_line_by_index(idx_default + idx + 1))["value"]

            params.append(
                {
                    "Name": name,
                    "Prompt": hint,
                    "Type": datatype,
                    "Value": default,
                }
            )

        return params

    def _get_variables(self) -> list:

        # Variables are a bit like the parameters with them
        # being defined over multiple lines in different sections

        # What does the json look like with no datasource?
        variables = []

        # variable names are from 577
        names = self._get_multiline_block(linecode=577)

        # offsets are from 579
        idx_offset = self._get_line_index_by_code(579)

        # types are from 578
        idx_types = self._get_line_index_by_code(578)

        # start and end bytes
        idx_start = self._get_line_index_by_code(580)
        idx_end = self._get_line_index_by_code(581)

        for idx, name in enumerate(names):

            # these are single ints on the line
            offset = int(self._get_line_by_index(idx_offset + idx + 1))
            type = self._type_mapping[int(self._get_line_by_index(idx_types + idx + 1))]

            # get start and end bytes
            start = int(self._get_line_by_index(idx_start + idx + 1))
            end = int(self._get_line_by_index(idx_end + idx + 1))

            #
            var = {"EndByte": end, "Name": name, "Position": offset, "StartByte": start, "Type": type}

            variables.append(var)

        return variables

    def _get_datasource(self) -> dict:

        # What does the json look like with no datasource?
        datasource = {}

        # need to come up with a mapping for all types
        datasource_type = self._parse_single_string(self._get_line_by_code(562))
        datasource_type_json = self._datasource_type_mapping[datasource_type]
        datasource["Type"] = datasource_type_json
        # I'm going to assume the delimiter type is always "Character" when source type is ASCII
        # obviously need to map other types if necessary
        if datasource_type_json == "ASCII":
            datasource["asciiDelimiterType"] = "Character"

        datasource["asciiDecimalSeparator"] = self._parse_single_string(self._get_line_by_code(588))
        datasource["asciiDelimiterChar"] = self._parse_single_string(self._get_line_by_code(567))

        datasource["asciiHeaderRecords"] = self._parse_single_int(self._get_line_by_code(569))
        datasource["asciiQuoteCharacter"] = self._parse_single_string(self._get_line_by_code(568))
        datasource["asciiThousandSeparator"] = self._parse_single_string(self._get_line_by_code(589))
        datasource["dataSourceNameForClient"] = self._parse_single_string(self._get_line_by_code(585))
        datasource["dataSourceNameForServer"] = self._parse_single_string(self._get_line_by_code(586))

        return datasource
        # this needs to be refactored
        # idx_datatype = self._get_line_index_by_code(561)
        # idx_default = self._get_line_index_by_code(590)
        # idx_hint = self._get_line_index_by_code(637)

        # names = self._get_multiline_block(linecode=560)

        # for idx, name in enumerate(names):

        #     # these are single ints on the line
        #     datatype = int(self._get_line_by_index(idx_datatype + idx + 1))

        #     hint = self._get_key_value_pair_string(self._get_line_by_index(idx_hint + idx + 1))["value"]

        #     default = self._get_key_value_pair_string(self._get_line_by_index(idx_default + idx + 1))["value"]

        #     params.append(
        #         {
        #             "Name": name,
        #             "Prompt": hint,
        #             "Type": datatype,
        #             "Value": default,
        #         }
        #     )

        # return params

    def _parse_single_int(self, line: str) -> int:
        """
        Read a line with a code and a single int value and return the value only
        """

        _, value = line.split(self.delimiter)

        return int(value)

    def _parse_single_string(self, line: str) -> str:
        """
        Read a value string containing a single string and return the value without quotes
        """

        # need to make this portable

        chunks = line.split(self.delimiter)

        value = str.join(",", chunks[1:])

        # hack for getting the delimiter - will need to be done better
        if value == '""""':
            return '"'

        return value.strip(self.quote_character)

    def _get_key_value_pair_string(self, line: str):

        # e.g. 'pPeriod,"All"'

        key = line.split(self.delimiter)[0]
        value = str.join("", line.split(self.delimiter)[1:]).strip(self.quote_character)

        return {"key": key, "value": value}

    def _get_key_value_pair_int(self, line: str, quote_character: str):

        # e.g. 'pLogging,0'

        key = line.split(self.delimiter)[0]
        value = int(line.split(self.delimiter)[1])

        return {"key": key, "value": value}

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

        # get the index and the line for this code
        index = self._get_line_index_by_code(linecode)
        line = self._get_line_by_code(linecode)

        # parse the line to get the number of lines
        number_of_lines = self._parse_single_int(line)

        lines = []

        # loop over the next n lines
        index = index + 1
        for i in range(index, index + number_of_lines):

            line = self._get_line_by_index(i)
            lines.append(line)

        return lines

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
