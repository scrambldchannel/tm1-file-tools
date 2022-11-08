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
    empty_code_tab_lines = ["", "#****Begin: Generated Statements***", "#****End: Generated Statements****"]

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

        for index, line in enumerate(lines):

            code = line.split(self.delimiter)[0]

            if code == str(linecode):
                value = str.join("", line[len(str(linecode)) + 1 :]).strip(self.quote_character)  # noqa
                return (line, code, value, index)

    def _get_line_by_index(self, index: int):

        lines = self.readlines()

        return lines[index]

    def to_json(self, sort_keys: bool = True):

        line, _, name, _ = self._get_line_by_code(602)

        _, prolog, _ = self._get_prolog_codeblock()
        _, metadata, _ = self._get_metadata_codeblock()
        _, data, _ = self._get_data_codeblock()
        _, epilog, _ = self._get_epilog_codeblock()

        prolog = self._codeblock_to_json_str(prolog)
        metadata = self._codeblock_to_json_str(metadata)
        data = self._codeblock_to_json_str(data)
        epilog = self._codeblock_to_json_str(epilog)

        _, _, security_access, _ = self._get_line_by_code(1217)
        security_access = security_access == 1

        parameters = self._get_parameters()

        json_dump = {
            "Name": name,
            "PrologProcedure": prolog,
            "MetadataProcedure": metadata,
            "DataProcedure": data,
            "EpilogProcedure": epilog,
            "HasSecurityAccess": security_access,
            "Parameters": parameters,
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
        _, _, _, idx_datatype = self._get_line_by_code(561)
        _, _, _, idx_default = self._get_line_by_code(590)
        _, _, _, idx_hint = self._get_line_by_code(637)

        _, names, _ = self._get_multiline_block(linecode=560)

        for idx, name in enumerate(names):

            datatype = self._parse_single_int(self._get_line_by_index(idx_datatype + idx + 1))

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
