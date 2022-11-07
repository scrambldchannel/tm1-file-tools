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
    assert p._get_line_by_code(linecode=601) == ("601,100", "601", "100", 0)
    # assert p._get_line_by_code(linecode=602) == ("602", "my zany process", 1)


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


def test_parse_single_int():

    line = "601,100"

    assert TM1ProcessFile._parse_single_int(line) == 100


def test_parse_single_str():

    line = '602,"my zany process"'

    assert TM1ProcessFile._parse_single_string(line) == "my zany process"


def test_get_multiline_block(json_dumps_folder):

    # create pro object from the file
    pro = TM1ProcessFile(Path.joinpath(json_dumps_folder, "processes", "new_process.pro"))

    number_of_lines, lines = pro._get_multiline_block(linecode=560)

    assert number_of_lines
