from pathlib import Path

from tm1filetools.files.text.linecode import TM1LinecodeFile, TM1LinecodeRowBase


def test_init(test_folder):

    p = TM1LinecodeFile(Path.joinpath(test_folder, "copy data from my cube.pro"))

    assert p.suffix == "pro"

    assert p.stem == "copy data from my cube"


def test_get_line_by_code(test_folder):

    p = TM1LinecodeFile(Path.joinpath(test_folder, "copy data from my cube.pro"))

    # build up this file and read some basic line codes

    p.write(
        r"""601,100
602,"my zany process"
        """
    )

    # line, code, value, index
    assert p._get_line_by_code(linecode=601) == "601,100"
    assert p._get_line_by_code(linecode=602) == '602,"my zany process"'


def test_get_lines_by_index(test_folder):

    p = TM1LinecodeFile(Path.joinpath(test_folder, "copy data from my cube.pro"))

    # build up this file and read some basic line codes

    p.write(
        r"""601,100
602,"my zany process"
        """
    )

    lines = p._get_lines_by_index(index=0, line_count=2, rstrip=True)
    assert len(lines) == 2
    assert lines[0] == "601,100"

    lines = p._get_lines_by_index(index=0, line_count=1, rstrip=False)
    assert len(lines) == 1
    assert lines[0] == "601,100\n"


def test_parse_single_int():

    line = "601,100"

    assert TM1LinecodeRowBase.parse_single_int(line) == 100

    line = "572,48"
    assert TM1LinecodeRowBase.parse_single_int(line) == 48


def test_parse_single_str():

    line = '602,"my zany process"'

    assert TM1LinecodeRowBase.parse_single_string(line=line) == "my zany process"

    line = '602,"my, zany process"'

    assert TM1LinecodeRowBase.parse_single_string(line=line) == "my, zany process"

    line = '602,"my, zany process"'

    assert TM1LinecodeRowBase.parse_single_string(line=line) == "my, zany process"


def test_parse_key_value_pair_str():

    line = 'pPeriod,"All"'

    assert TM1LinecodeFile.parse_key_value_pair_string(line=line) == {"key": "pPeriod", "value": "All"}


def test_parse_key_value_pair_int():

    line = "pLogging,1"

    assert TM1LinecodeFile.parse_key_value_pair_int(line=line) == {"key": "pLogging", "value": 1}
