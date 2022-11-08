from pathlib import Path

from tm1filetools.files.text.linecode import TM1LinecodeFile


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


def test_get_line_by_index(test_folder):

    p = TM1LinecodeFile(Path.joinpath(test_folder, "copy data from my cube.pro"))

    # build up this file and read some basic line codes

    p.write(
        r"""601,100
602,"my zany process"
        """
    )

    assert p._get_line_by_index(index=0) == "601,100"
    assert p._get_line_by_index(index=1) == '602,"my zany process"'


def test_parse_single_int():

    # pro = TM1LinecodeFile(Path.joinpath(json_dumps_folder, "processes", "new_process.pro"))

    line = "601,100"

    assert TM1LinecodeFile._parse_single_int(line) == 100

    line = "572,48"
    assert TM1LinecodeFile._parse_single_int(line) == 48


def test_parse_single_str():

    line = '602,"my zany process"'

    assert TM1LinecodeFile._parse_single_string(line=line) == "my zany process"

    line = '602,"my, zany process"'

    assert TM1LinecodeFile._parse_single_string(line=line) == "my, zany process"

    line = '602,"my, zany process"'

    assert TM1LinecodeFile._parse_single_string(line=line) == "my, zany process"


def test_parse_key_value_pair_str():

    line = 'pPeriod,"All"'

    assert TM1LinecodeFile._get_key_value_pair_string(line=line) == {"key": "pPeriod", "value": "All"}


def test_parse_key_value_pair_int():

    line = "pLogging,1"

    assert TM1LinecodeFile._get_key_value_pair_int(line=line) == {"key": "pLogging", "value": 1}


def test_get_multiline_block(json_dumps_folder):

    # create pro object from the file
    pro = TM1LinecodeFile(Path.joinpath(json_dumps_folder, "processes", "new_process.pro"))

    lines = pro._get_multiline_block(linecode=572)

    # lines should be correct here
    assert len(lines) == 48

    assert lines[0] == ""
    assert lines[2] == "#****End: Generated Statements****"
    assert lines[4] == "#####  LOGGING"
    # check indent
    assert lines[40] == "   'pCubeLogging', 0,"

    assert lines[-1] == ""
