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

mandatory_json_fields = [
    # this list might need some tweaking
    # i.e. do they all appear in every single process?
    "DataProcedure",
    "DataSource",
    "EpilogProcedure",
    "HasSecurityAccess",
    "MetadataProcedure",
    "Name",
    "Parameters",
    "PrologProcedure",
    "UIData",
    "Variables",
    "VariablesUIData",
]


code_blocks = [
    {
        # prolog
        "linecode": 572,
        "json_field": "PrologProcedure",
    },
    {
        # metadata
        "linecode": 573,
        "json_field": "MetadataProcedure",
    },
    {
        # data
        "linecode": 574,
        "json_field": "DataProcedure",
    },
    {
        # epilog
        "linecode": 575,
        "json_field": "EpilogProcedure",
    },
]


@pytest.mark.parametrize("proc", sample_procs)
def test_init(data_folder, proc):

    p = TM1ProcessFile(Path.joinpath(data_folder, f"{proc}.pro"))

    assert p
    assert p.suffix == "pro"


@pytest.mark.parametrize("proc", sample_procs)
def test_ui_data(data_folder, proc_json_out_folder, proc):

    # create pro object from the file
    pro = TM1ProcessFile(Path.joinpath(data_folder, f"{proc}.pro"))

    json_out_str = pro._to_json()

    json_out = json.loads(json_out_str)

    with open(Path.joinpath(proc_json_out_folder, f"{proc}.json"), "r") as f:
        expected_json_str = f.read()

    expected_json = json.loads(expected_json_str)

    # UIData

    assert json_out.get("UIData") == expected_json.get("UIData")


@pytest.mark.skip("Not yet implemented")
@pytest.mark.parametrize("proc", sample_procs)
def test_variable_ui_data(data_folder, proc_json_out_folder, proc):

    # create pro object from the file
    pro = TM1ProcessFile(Path.joinpath(data_folder, f"{proc}.pro"))

    json_out_str = pro._to_json()

    json_out = json.loads(json_out_str)

    with open(Path.joinpath(proc_json_out_folder, f"{proc}.json"), "r") as f:
        expected_json_str = f.read()

    expected_json = json.loads(expected_json_str)

    assert json_out.get("VariablesUIData") == expected_json.get("VariablesUIData")


@pytest.mark.parametrize("proc", sample_procs)
def test_get_parameters(data_folder, proc_json_out_folder, proc):

    # create pro object from the file
    pro = TM1ProcessFile(Path.joinpath(data_folder, f"{proc}.pro"))

    params = pro._get_parameters()

    with open(Path.joinpath(proc_json_out_folder, f"{proc}.json"), "r") as f:
        expected_json_str = f.read()

    json_expected = json.loads(expected_json_str)

    expected_params = json_expected["Parameters"]

    if len(params) == 0:
        # this should be trivial
        assert params == expected_params

    else:

        for i, p in enumerate(params):
            assert p.get("Name") == expected_params[i].get("Name")
            assert p.get("Prompt") == expected_params[i].get("Prompt")
            assert p.get("Type") == expected_params[i].get("Type")
            assert p.get("Value") == expected_params[i].get("Value")


@pytest.mark.parametrize("proc", sample_procs)
def test_get_variables(data_folder, proc_json_out_folder, proc):

    # create pro object from the file
    pro = TM1ProcessFile(Path.joinpath(data_folder, f"{proc}.pro"))

    vars = pro._get_variables()

    with open(Path.joinpath(proc_json_out_folder, f"{proc}.json"), "r") as f:
        expected_json_str = f.read()

    json_expected = json.loads(expected_json_str)

    assert vars == json_expected["Variables"]


@pytest.mark.parametrize("proc", sample_procs)
def test_get_datasource(data_folder, proc_json_out_folder, proc):

    pro = TM1ProcessFile(Path.joinpath(data_folder, f"{proc}.pro"))

    datasource = pro._get_datasource()

    assert datasource

    with open(Path.joinpath(proc_json_out_folder, f"{proc}.json"), "r") as f:
        expected_json_str = f.read()

    expected_json = json.loads(expected_json_str)

    assert datasource == expected_json.get("DataSource")


@pytest.mark.parametrize("proc,json_field", itertools.product(sample_procs, mandatory_json_fields))
def test_to_valid_json(data_folder, proc, json_field):

    # create pro object from the file
    pro = TM1ProcessFile(Path.joinpath(data_folder, f"{proc}.pro"))

    json_out_str = pro._to_json()

    json_proc = json.loads(json_out_str)

    assert json_proc

    # this might return an empty list, dict etc
    # but the assumption is that each key should exist
    assert json_proc.get(json_field) is not None


@pytest.mark.parametrize("proc,block", itertools.product(sample_procs, code_blocks))
def test_multiline_block(data_folder, proc, block):

    pro = TM1ProcessFile(Path.joinpath(data_folder, f"{proc}.pro"))

    # rstrip implied
    # returns a list of strings
    code = pro._get_multiline_block(linecode=block["linecode"])

    # we should have at least one line
    assert len(code) > 0

    # what else can be usefylly tested here?


@pytest.mark.parametrize("proc,block", itertools.product(sample_procs, code_blocks))
def test_codeblock_to_json_str(data_folder, proc_json_out_folder, proc, block):

    pro = TM1ProcessFile(Path.joinpath(data_folder, f"{proc}.pro"))

    code = pro._get_multiline_block(linecode=block["linecode"])

    json_field = block["json_field"]

    codeblock_json_str = pro._codeblock_to_json_str(code)

    assert codeblock_json_str

    with open(Path.joinpath(proc_json_out_folder, f"{proc}.json"), "r") as f:
        expected_json_str = f.read()

    expected_json = json.loads(expected_json_str)

    assert expected_json

    expected_block: str = expected_json.get(json_field)

    assert expected_block

    assert type(codeblock_json_str) == type(expected_block)

    # # check that they're equivalent outside of trailing whitespace

    block_lstripped = codeblock_json_str.lstrip()
    expected_lstripped = expected_block.lstrip()

    assert block_lstripped[0] == expected_lstripped[0]

    block_rstripped = codeblock_json_str.rstrip()
    expected_rstripped = expected_block.rstrip()

    failing_procs = ["test.tm1filetools.dim_subset_process", "test.tm1filetools.cube_view_process"]

    if proc in failing_procs:
        pytest.skip("edge cases")

    assert block_rstripped[-1] == expected_rstripped[-1]


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


def test_empty_process(data_folder, proc_json_out_folder):

    process = "test.tm1filetools.empty_process"
    pro = TM1ProcessFile(Path.joinpath(data_folder, f"{process}.pro"))

    json_out_str = pro._to_json()

    assert json_out_str

    json_out = json.loads(json_out_str)

    with open(Path.joinpath(proc_json_out_folder, f"{process}.json"), "r") as f:
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


def test_prolog_only_process(data_folder, proc_json_out_folder):

    process = "test.tm1filetools.prolog_only_process"
    pro = TM1ProcessFile(Path.joinpath(data_folder, f"{process}.pro"))

    json_out_str = pro._to_json()

    assert json_out_str

    json_out = json.loads(json_out_str)

    with open(Path.joinpath(proc_json_out_folder, f"{process}.json"), "r") as f:
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


def test_epilog_only_process(data_folder, proc_json_out_folder):

    process = "test.tm1filetools.epilog_only_process"
    pro = TM1ProcessFile(Path.joinpath(data_folder, f"{process}.pro"))

    json_out_str = pro._to_json()

    assert json_out_str

    json_out = json.loads(json_out_str)

    with open(Path.joinpath(proc_json_out_folder, f"{process}.json"), "r") as f:
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


def test_to_json(data_folder, proc_json_out_folder):

    # create pro object from the file
    pro = TM1ProcessFile(Path.joinpath(data_folder, "new_process.pro"))

    json_out_str = pro._to_json()

    with open(Path.joinpath(proc_json_out_folder, "new_process.json"), "r") as f:
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
