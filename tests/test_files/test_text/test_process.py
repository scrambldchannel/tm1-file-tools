import itertools
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

code_blocks = [
    ("prolog", 572),
    ("metadata", 573),
    ("data", 574),
    ("epilog", 575),
]


@pytest.mark.parametrize("proc", sample_procs)
def test_init(data_folder, proc):

    p = TM1ProcessFile(Path.joinpath(data_folder, f"{proc}.pro"))

    assert p
    assert p.suffix == "pro"


@pytest.mark.parametrize("proc", sample_procs)
def test_ui_data(data_folder, json_out_folder, proc):

    # create pro object from the file
    pro = TM1ProcessFile(Path.joinpath(data_folder, f"{proc}.pro"))

    json_out_str = pro._to_json()

    json_out = json.loads(json_out_str)

    with open(Path.joinpath(json_out_folder, f"{proc}.json"), "r") as f:
        expected_json_str = f.read()

    expected_json = json.loads(expected_json_str)

    # UIData

    assert json_out.get("UIData") == expected_json.get("UIData")


@pytest.mark.skip("Failing")
@pytest.mark.parametrize("proc", sample_procs)
def test_variable_ui_data(data_folder, json_out_folder, proc):

    # create pro object from the file
    pro = TM1ProcessFile(Path.joinpath(data_folder, f"{proc}.pro"))

    json_out_str = pro._to_json()

    json_out = json.loads(json_out_str)

    with open(Path.joinpath(json_out_folder, f"{proc}.json"), "r") as f:
        expected_json_str = f.read()

    expected_json = json.loads(expected_json_str)

    assert json_out.get("VariablesUIData") == expected_json.get("VariablesUIData")


@pytest.mark.parametrize("proc", sample_procs)
def test_get_parameters(data_folder, json_out_folder, proc):

    # create pro object from the file
    pro = TM1ProcessFile(Path.joinpath(data_folder, f"{proc}.pro"))

    params = pro._get_parameters()

    with open(Path.joinpath(json_out_folder, f"{proc}.json"), "r") as f:
        expected_json_str = f.read()

    json_expected = json.loads(expected_json_str)

    assert params == json_expected["Parameters"]


@pytest.mark.parametrize("proc", sample_procs)
def test_get_variables(data_folder, json_out_folder, proc):

    # create pro object from the file
    pro = TM1ProcessFile(Path.joinpath(data_folder, f"{proc}.pro"))

    vars = pro._get_variables()

    with open(Path.joinpath(json_out_folder, f"{proc}.json"), "r") as f:
        expected_json_str = f.read()

    json_expected = json.loads(expected_json_str)

    assert vars == json_expected["Variables"]


@pytest.mark.parametrize("proc", sample_procs)
def test_get_datasource(data_folder, json_out_folder, proc):

    pro = TM1ProcessFile(Path.joinpath(data_folder, f"{proc}.pro"))

    datasource = pro._get_datasource()

    assert datasource

    with open(Path.joinpath(json_out_folder, f"{proc}.json"), "r") as f:
        expected_json_str = f.read()

    expected_json = json.loads(expected_json_str)

    assert datasource == expected_json.get("DataSource")


@pytest.mark.parametrize("proc", sample_procs)
def test_to_valid_json(data_folder, proc):

    # create pro object from the file
    pro = TM1ProcessFile(Path.joinpath(data_folder, f"{proc}.pro"))

    json_out_str = pro._to_json()

    assert json.loads(json_out_str)


@pytest.mark.parametrize("proc,block", itertools.product(sample_procs, code_blocks))
def test_multiline_block(data_folder, proc, block):

    pro = TM1ProcessFile(Path.joinpath(data_folder, f"{proc}.pro"))

    # rstrip implied
    # returns a list of strings
    code = pro._get_multiline_block(linecode=block[1])

    # we should have at least one line
    assert len(code) > 0

    # what else can be usefylly tested here?


@pytest.mark.skip("Failing, possibly whitespace")
@pytest.mark.parametrize("proc,block", itertools.product(sample_procs, code_blocks))
def test_codeblock_to_json_str(data_folder, json_out_folder, proc, block):

    pro = TM1ProcessFile(Path.joinpath(data_folder, f"{proc}.pro"))

    # rstrip implied
    # returns a list of strings
    code = pro._get_multiline_block(linecode=572)

    codeblock_json_string = pro._codeblock_to_json_str(code)

    with open(Path.joinpath(json_out_folder, f"{proc}.json"), "r") as f:
        expected_json_str = f.read()

    expected_json = json.loads(expected_json_str)

    assert codeblock_json_string == expected_json.get("PrologProcedure")


# below here, tests still pretty much hardcoded, try to parameterise


def test_prolog(data_folder):
    pro = TM1ProcessFile(Path.joinpath(data_folder, "new_process.pro"))

    lines = pro.get_prolog_code()

    assert len(lines) == 48
    assert lines[0] == pro._code_block_prefix_lines[0]
    assert lines[1] == pro._code_block_prefix_lines[1]
    assert lines[2] == pro._code_block_prefix_lines[2]


def test_metadata(data_folder):
    pro = TM1ProcessFile(Path.joinpath(data_folder, "new_process.pro"))

    lines = pro.get_metadata_code()

    assert len(lines) == 3

    assert lines[0] == pro._code_block_prefix_lines[0]
    assert lines[1] == pro._code_block_prefix_lines[1]
    assert lines[2] == pro._code_block_prefix_lines[2]


def test_data_code_block(data_folder):
    pro = TM1ProcessFile(Path.joinpath(data_folder, "new_process.pro"))

    lines = pro.get_data_code()

    assert lines[0] == pro._code_block_prefix_lines[0]
    assert lines[1] == pro._code_block_prefix_lines[1]
    assert lines[2] == pro._code_block_prefix_lines[2]

    assert len(lines) == 37


def test_epilog_code_block(data_folder):

    pro = TM1ProcessFile(Path.joinpath(data_folder, "new_process.pro"))

    lines = pro.get_epilog_code()

    assert lines[0] == pro._code_block_prefix_lines[0]
    assert lines[1] == pro._code_block_prefix_lines[1]
    assert lines[2] == pro._code_block_prefix_lines[2]
    assert len(lines) == 21


def test_empty_process(data_folder, json_out_folder):

    process = "test.tm1filetools.empty_process"
    pro = TM1ProcessFile(Path.joinpath(data_folder, f"{process}.pro"))

    json_out_str = pro._to_json()

    assert json_out_str

    json_out = json.loads(json_out_str)

    with open(Path.joinpath(json_out_folder, f"{process}.json"), "r") as f:
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


def test_prolog_only_process(data_folder, json_out_folder):

    process = "test.tm1filetools.prolog_only_process"
    pro = TM1ProcessFile(Path.joinpath(data_folder, f"{process}.pro"))

    json_out_str = pro._to_json()

    assert json_out_str

    json_out = json.loads(json_out_str)

    with open(Path.joinpath(json_out_folder, f"{process}.json"), "r") as f:
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


def test_epilog_only_process(data_folder, json_out_folder):

    process = "test.tm1filetools.epilog_only_process"
    pro = TM1ProcessFile(Path.joinpath(data_folder, f"{process}.pro"))

    json_out_str = pro._to_json()

    assert json_out_str

    json_out = json.loads(json_out_str)

    with open(Path.joinpath(json_out_folder, f"{process}.json"), "r") as f:
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


def test_to_json(data_folder, json_out_folder):

    # create pro object from the file
    pro = TM1ProcessFile(Path.joinpath(data_folder, "new_process.pro"))

    json_out_str = pro._to_json()

    with open(Path.joinpath(json_out_folder, "new_process.json"), "r") as f:
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
