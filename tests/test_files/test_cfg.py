from pathlib import Path

from tm1filetools.files.cfg import TM1CfgFile


def test_read_and_write(test_folder):

    f = TM1CfgFile(Path.joinpath(test_folder, "tm1.cfg"))

    # need to create the section
    f.config.add_section(f._section)

    param = "IntegratedSecurityMode"

    assert f.get_parameter(param) is None

    value = "1"

    f.set_parameter(param, value)

    assert f.get_parameter(param) == value

    # also re-open file to check it's been written to disk

    f2 = TM1CfgFile(Path.joinpath(test_folder, "tm1.cfg"))

    assert f2.get_parameter(param) == value
