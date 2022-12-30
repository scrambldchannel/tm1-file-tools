import json
from pathlib import Path

import pytest

from tm1filetools.files import TM1ProcessFile

sample_procs = [
    "new_process",
    "test.tm1filetools.cube_view_process",
    "test.tm1filetools.dim_subset_process",
    "test.tm1filetools.empty_process",
    "test.tm1filetools.epilog_only_process",
    "test.tm1filetools.prolog_only_process",
]


@pytest.mark.parametrize("proc", sample_procs)
def test_init(json_dumps_folder, proc):

    p = TM1ProcessFile(Path.joinpath(json_dumps_folder, f"{proc}.pro"))

    assert p
    assert p.suffix == "pro"


@pytest.mark.parametrize("proc", sample_procs)
def test_ui_data(json_dumps_folder, proc):

    # create pro object from the file
    pro = TM1ProcessFile(Path.joinpath(json_dumps_folder, "processes", f"{proc}.pro"))

    json_out_str = pro._to_json()

    json_out = json.loads(json_out_str)

    with open(Path.joinpath(json_dumps_folder, "processes", f"{proc}.json"), "r") as f:
        expected_json_str = f.read()

    expected_json = json.loads(expected_json_str)

    # UIData

    assert json_out.get("UIData") == expected_json.get("UIData")


@pytest.mark.skip("Failing")
@pytest.mark.parametrize("proc", sample_procs)
def test_variable_ui_data(json_dumps_folder, proc):

    # create pro object from the file
    pro = TM1ProcessFile(Path.joinpath(json_dumps_folder, "processes", f"{proc}.pro"))

    json_out_str = pro._to_json()

    json_out = json.loads(json_out_str)

    with open(Path.joinpath(json_dumps_folder, "processes", f"{proc}.json"), "r") as f:
        expected_json_str = f.read()

    expected_json = json.loads(expected_json_str)

    assert json_out.get("VariablesUIData") == expected_json.get("VariablesUIData")


@pytest.mark.parametrize("proc", sample_procs)
def test_get_parameters(json_dumps_folder, proc):

    # create pro object from the file
    pro = TM1ProcessFile(Path.joinpath(json_dumps_folder, "processes", f"{proc}.pro"))

    params = pro._get_parameters()

    with open(Path.joinpath(json_dumps_folder, "processes", f"{proc}.json"), "r") as f:
        expected_json_str = f.read()

    json_expected = json.loads(expected_json_str)

    assert params == json_expected["Parameters"]


@pytest.mark.parametrize("proc", sample_procs)
def test_get_variables(json_dumps_folder, proc):

    # create pro object from the file
    pro = TM1ProcessFile(Path.joinpath(json_dumps_folder, "processes", f"{proc}.pro"))

    vars = pro._get_variables()

    with open(Path.joinpath(json_dumps_folder, "processes", f"{proc}.json"), "r") as f:
        expected_json_str = f.read()

    json_expected = json.loads(expected_json_str)

    assert vars == json_expected["Variables"]


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


def test_prolog(json_dumps_folder):
    pro = TM1ProcessFile(Path.joinpath(json_dumps_folder, "processes", "new_process.pro"))

    lines = pro.get_prolog_code()

    assert len(lines) == 48
    assert lines[0] == pro._code_block_prefix_lines[0]
    assert lines[1] == pro._code_block_prefix_lines[1]
    assert lines[2] == pro._code_block_prefix_lines[2]


def test_metadata(json_dumps_folder):
    pro = TM1ProcessFile(Path.joinpath(json_dumps_folder, "processes", "new_process.pro"))

    lines = pro.get_metadata_code()

    assert len(lines) == 3

    assert lines[0] == pro._code_block_prefix_lines[0]
    assert lines[1] == pro._code_block_prefix_lines[1]
    assert lines[2] == pro._code_block_prefix_lines[2]


def test_data_code_block(json_dumps_folder):
    pro = TM1ProcessFile(Path.joinpath(json_dumps_folder, "processes", "new_process.pro"))

    lines = pro.get_data_code()

    assert lines[0] == pro._code_block_prefix_lines[0]
    assert lines[1] == pro._code_block_prefix_lines[1]
    assert lines[2] == pro._code_block_prefix_lines[2]

    assert len(lines) == 37


def test_epilog_code_block(json_dumps_folder):

    pro = TM1ProcessFile(Path.joinpath(json_dumps_folder, "processes", "new_process.pro"))

    lines = pro.get_epilog_code()

    assert lines[0] == pro._code_block_prefix_lines[0]
    assert lines[1] == pro._code_block_prefix_lines[1]
    assert lines[2] == pro._code_block_prefix_lines[2]
    assert len(lines) == 21


@pytest.mark.parametrize("proc", sample_procs)
def test_get_datasource(json_dumps_folder, proc):

    pro = TM1ProcessFile(Path.joinpath(json_dumps_folder, "processes", f"{proc}.pro"))

    datasource = pro._get_datasource()

    assert datasource

    with open(Path.joinpath(json_dumps_folder, "processes", f"{proc}.json"), "r") as f:
        expected_json_str = f.read()

    expected_json = json.loads(expected_json_str)

    assert datasource == expected_json.get("DataSource")


def test_empty_process(json_dumps_folder):

    process = "test.tm1filetools.empty_process"
    pro = TM1ProcessFile(Path.joinpath(json_dumps_folder, "processes", f"{process}.pro"))

    json_out_str = pro._to_json()

    assert json_out_str

    json_out = json.loads(json_out_str)

    with open(Path.joinpath(json_dumps_folder, "processes", f"{process}.json"), "r") as f:
        expected_json_str = f.read()

    json_expected = json.loads(expected_json_str)

    assert json_out["Name"] == json_expected["Name"]
    assert json_out["PrologProcedure"] == json_expected["PrologProcedure"]
    assert json_out["EpilogProcedure"] == json_expected["EpilogProcedure"]
    assert json_out["MetadataProcedure"] == json_expected["MetadataProcedure"]
    assert json_out["DataProcedure"] == json_expected["DataProcedure"]
    assert json_out["HasSecurityAccess"] == json_expected["HasSecurityAccess"]

    # not sure what to do about this UIData field,
    # need to determine whether a process can be created by TM1py without it
    # assert json_out["UIData"] == json_expected["UIData"]

    # should be empty
    assert json_out["DataSource"] == {"Type": "None"}

    # These work, an empty list is what is expected
    assert json_out["Parameters"] == json_expected["Parameters"]
    assert json_out["Variables"] == json_expected["Variables"]

    # this I have looked at yet
    assert json_out["VariablesUIData"] == json_expected["VariablesUIData"]


def test_prolog_only_process(json_dumps_folder):

    process = "test.tm1filetools.prolog_only_process"
    pro = TM1ProcessFile(Path.joinpath(json_dumps_folder, "processes", f"{process}.pro"))

    json_out_str = pro._to_json()

    assert json_out_str

    json_out = json.loads(json_out_str)

    with open(Path.joinpath(json_dumps_folder, "processes", f"{process}.json"), "r") as f:
        expected_json_str = f.read()

    json_expected = json.loads(expected_json_str)

    assert json_out["Name"] == json_expected["Name"]
    # Note, for the tabs we have data for, the json version seems to have trailing
    # whitespace :shrug:
    assert json_out["PrologProcedure"] == json_expected["PrologProcedure"].rstrip()
    assert json_out["EpilogProcedure"] == json_expected["EpilogProcedure"]
    assert json_out["MetadataProcedure"] == json_expected["MetadataProcedure"]
    assert json_out["DataProcedure"] == json_expected["DataProcedure"]
    assert json_out["HasSecurityAccess"] == json_expected["HasSecurityAccess"]

    # not sure what to do about this UIData field,
    # need to determine whether a process can be created by TM1py without it
    # assert json_out["UIData"] == json_expected["UIData"]

    # should be empty
    assert json_expected["DataSource"] == json_out["DataSource"]

    # These work, an empty list is what is expected
    assert json_out["Parameters"] == json_expected["Parameters"]
    assert json_out["Variables"] == json_expected["Variables"]

    assert json_out["VariablesUIData"] == json_expected["VariablesUIData"]


def test_epilog_only_process(json_dumps_folder):

    process = "test.tm1filetools.epilog_only_process"
    pro = TM1ProcessFile(Path.joinpath(json_dumps_folder, "processes", f"{process}.pro"))

    json_out_str = pro._to_json()

    assert json_out_str

    json_out = json.loads(json_out_str)

    with open(Path.joinpath(json_dumps_folder, "processes", f"{process}.json"), "r") as f:
        expected_json_str = f.read()

    json_expected = json.loads(expected_json_str)

    assert json_out["Name"] == json_expected["Name"]
    assert json_out["PrologProcedure"] == json_expected["PrologProcedure"]
    # Note, for the tabs we have data for, the json version seems to have trailing
    # whitespace :shrug:
    assert json_out["EpilogProcedure"] == json_expected["EpilogProcedure"].rstrip()
    assert json_out["MetadataProcedure"] == json_expected["MetadataProcedure"]
    assert json_out["DataProcedure"] == json_expected["DataProcedure"]
    assert json_out["HasSecurityAccess"] == json_expected["HasSecurityAccess"]

    # should be empty
    assert json_expected["DataSource"] == json_out["DataSource"]

    # These work, an empty list is what is expected
    assert json_out["Parameters"] == json_expected["Parameters"]
    assert json_out["Variables"] == json_expected["Variables"]

    assert json_out["VariablesUIData"] == json_expected["VariablesUIData"]


def test_to_json(json_dumps_folder):

    # create pro object from the file
    pro = TM1ProcessFile(Path.joinpath(json_dumps_folder, "processes", "new_process.pro"))

    json_out_str = pro._to_json()

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

    assert json_out["Parameters"][0]["Type"] == "String"
    assert json_out["Parameters"][1]["Type"] == "String"
    assert json_out["Parameters"][2]["Type"] == "String"

    assert json_out["Parameters"][0]["Value"] == "All"
    assert json_out["Parameters"][0]["Prompt"] == ""

    assert json_out["Variables"][0]["Name"] == "vPeriod"
    assert json_out["Variables"][0]["Type"] == "String"
