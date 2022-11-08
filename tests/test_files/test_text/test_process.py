import json
from pathlib import Path

from tm1filetools.files import TM1ProcessFile


def test_init(test_folder):

    p = TM1ProcessFile(Path.joinpath(test_folder, "copy data from my cube.pro"))

    assert p
    assert p.suffix == "pro"


def test_get_line_by_code(test_folder):

    p = TM1ProcessFile(Path.joinpath(test_folder, "copy data from my cube.pro"))

    # build up this file and read some basic line codes

    p.write(
        r"""601,100
602,"my zany process"
        """
    )

    # line, code, value, index
    assert p._get_line_by_code(linecode=601) == "601,100"
    assert p._get_line_by_code(linecode=602) == '602,"my zany process"'


def test_get_line_by_index(test_folder):

    p = TM1ProcessFile(Path.joinpath(test_folder, "copy data from my cube.pro"))

    # build up this file and read some basic line codes

    p.write(
        r"""601,100
602,"my zany process"
        """
    )

    assert p._get_line_by_index(index=0) == "601,100"
    assert p._get_line_by_index(index=1) == '602,"my zany process"'


def test_to_json(json_dumps_folder):

    # create pro object from the file
    pro = TM1ProcessFile(Path.joinpath(json_dumps_folder, "processes", "new_process.pro"))

    json_out_str = pro.to_json()

    with open(Path.joinpath(json_dumps_folder, "processes", "new_process.json"), "r") as f:
        expected_json_str = f.read()

    json_expected = json.loads(expected_json_str)

    assert json_out_str

    json_out = json.loads(json_out_str)

    assert json_out["Name"] == "new process"
    assert json_out["Name"] == json_expected["Name"]

    assert json_out["PrologProcedure"][0] == json_expected["PrologProcedure"][0]
    assert json_out["PrologProcedure"][5] == json_expected["PrologProcedure"][5]
    assert json_out["PrologProcedure"][12] == json_expected["PrologProcedure"][12]

    assert json_out["MetadataProcedure"] == json_expected["MetadataProcedure"]
    assert json_out["DataProcedure"] == json_expected["DataProcedure"]
    assert json_out["EpilogProcedure"] == json_expected["EpilogProcedure"]

    assert json_out["HasSecurityAccess"] is False
    assert json_out["HasSecurityAccess"] == json_expected["HasSecurityAccess"]

    assert json_out["Parameters"][0]["Name"] == "pPeriod"
    assert json_out["Parameters"][1]["Name"] == "pVersion"
    assert json_out["Parameters"][2]["Name"] == "pScenario"

    assert json_out["Parameters"][0]["Type"] == 2
    assert json_out["Parameters"][1]["Type"] == 2
    assert json_out["Parameters"][2]["Type"] == 2

    assert json_out["Parameters"][0]["Value"] == "All"
    assert json_out["Parameters"][0]["Prompt"] == ""


def test_parse_single_int(json_dumps_folder):

    pro = TM1ProcessFile(Path.joinpath(json_dumps_folder, "processes", "new_process.pro"))

    line = pro._get_line_by_code(601)
    assert pro._parse_single_int(line) == 100

    line = pro._get_line_by_code(572)
    assert pro._parse_single_int(line) == 48


def test_parse_single_str(json_dumps_folder):

    pro = TM1ProcessFile(Path.joinpath(json_dumps_folder, "processes", "new_process.pro"))

    line = '602,"my zany process"'

    assert pro._parse_single_string(line=line) == "my zany process"

    line = '602,"my, zany process"'

    assert pro._parse_single_string(line=line) == "my, zany process"

    line = '602,"my, zany process"'

    assert pro._parse_single_string(line=line) == "my, zany process"


def test_get_multiline_block(json_dumps_folder):

    # create pro object from the file
    pro = TM1ProcessFile(Path.joinpath(json_dumps_folder, "processes", "new_process.pro"))

    lines = pro._get_multiline_block(linecode=572)

    # lines should be correct here
    assert len(lines) == 48

    assert lines[0] == ""
    assert lines[2] == "#****End: Generated Statements****"
    assert lines[4] == "#####  LOGGING"
    # check indent
    assert lines[40] == "   'pCubeLogging', 0,"

    assert lines[-1] == ""


def test_codeblock_to_json(json_dumps_folder):

    pro = TM1ProcessFile(Path.joinpath(json_dumps_folder, "processes", "new_process.pro"))

    lines = pro._get_multiline_block(linecode=572)

    assert lines[0] == ""
    assert len(lines) == 48

    json_codeblock = pro._codeblock_to_json_str(lines)

    expected_json_codeblock = "\r\n#****Begin: Generated Statements***\r\n#****End: Generated Statements****\r\n\r\n#####  LOGGING\r\nNumericGlobalVariable('MetadataMinorErrorCount');\r\nNumericGlobalVariable('PrologMinorErrorCount');\r\nNumericGlobalVariable('DataMinorErrorCount');\r\nsProcName = GetPRocessName();\r\n# This line needs to be changed for each process\r\nsParams = '';\r\nExecuteProcess('process_logging.start', 'pProcess', sProcName , 'pParams', sParams);\r\n#####  END LOGGING\r\n\r\n\r\nsCube = 'FX Rates';\r\n\r\n\r\n\r\nif(pPeriod @<> 'All');\r\n  sFilter =  'Version| ' | pVersion |  '& Scenario| Baseline & Publication | Working & Period |' | pPeriod;\r\nElse;\r\n  sFilter =  'Version| ' | pVersion |  '& Scenario| Baseline & Publication | Working';\r\nEndIf;\r\n\r\n\r\n\r\nExecuteProcess(\r\n  '}bedrock.cube.data.clear',\r\n  'pLogOutput', 1,\r\n  'pStrictErrorHandling', 1,\r\n  'pCube', sCube,\r\n   'pView', '',\r\n   'pFilter', '',\r\n   'pFilterParallel', '',\r\n   'pParallelThreads', 0,\r\n   'pDimDelim', '&',\r\n   'pEleStartDelim', '|',\r\n   'pEleDelim', '+',\r\n   'pSuppressConsolStrings', 0,\r\n   'pCubeLogging', 0,\r\n   'pTemp', 1,\r\n   'pSandbox', '',\r\n   'pSubN', 0\r\n);\r\n\r\n\r\n"  # noqa

    assert json_codeblock[0] == "\r"
    assert json_codeblock[0] == expected_json_codeblock[0]

    assert json_codeblock[1] == "\n"
    assert json_codeblock[1] == expected_json_codeblock[1]

    assert json_codeblock[2] == "#"
    assert json_codeblock[2] == expected_json_codeblock[2]

    assert json_codeblock[45] == expected_json_codeblock[45]

    assert json_codeblock[200] == expected_json_codeblock[200]
    assert json_codeblock[250] == expected_json_codeblock[250]
    assert json_codeblock[300] == expected_json_codeblock[300]
    assert json_codeblock[325] == expected_json_codeblock[325]
    assert json_codeblock[332] == "'"
    assert json_codeblock[332] == expected_json_codeblock[332]
    assert json_codeblock[333] == ";"
    assert json_codeblock[333] == expected_json_codeblock[333]

    # Bradman's number seems to be wherer the problem is
    assert json_codeblock[334] == "\r"

    assert json_codeblock[334] == expected_json_codeblock[334]

    # lenth comparison
    len_cb, len_exp = len(json_codeblock), len(expected_json_codeblock)
    assert len_cb == len_exp


def test_prolog_code_block(json_dumps_folder):
    pro = TM1ProcessFile(Path.joinpath(json_dumps_folder, "processes", "new_process.pro"))

    lines = pro._get_prolog_codeblock()

    assert len(lines) == 48
    assert lines[0] == pro._code_block_prefix_lines[0]
    assert lines[1] == pro._code_block_prefix_lines[1]
    assert lines[2] == pro._code_block_prefix_lines[2]


def test_metadata_code_block(json_dumps_folder):
    pro = TM1ProcessFile(Path.joinpath(json_dumps_folder, "processes", "new_process.pro"))

    lines = pro._get_metadata_codeblock()

    assert len(lines) == 3

    assert lines[0] == pro._code_block_prefix_lines[0]
    assert lines[1] == pro._code_block_prefix_lines[1]
    assert lines[2] == pro._code_block_prefix_lines[2]


def test_data_code_block(json_dumps_folder):
    pro = TM1ProcessFile(Path.joinpath(json_dumps_folder, "processes", "new_process.pro"))

    lines = pro._get_data_codeblock()

    assert lines[0] == pro._code_block_prefix_lines[0]
    assert lines[1] == pro._code_block_prefix_lines[1]
    assert lines[2] == pro._code_block_prefix_lines[2]

    assert len(lines) == 37


def test_epilog_code_block(json_dumps_folder):
    pro = TM1ProcessFile(Path.joinpath(json_dumps_folder, "processes", "new_process.pro"))

    lines = pro._get_epilog_codeblock()

    assert lines[0] == pro._code_block_prefix_lines[0]
    assert lines[1] == pro._code_block_prefix_lines[1]
    assert lines[2] == pro._code_block_prefix_lines[2]
    assert len(lines) == 21
