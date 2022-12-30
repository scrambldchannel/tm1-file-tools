from pathlib import Path

from tm1filetools.files import TM1CfgFile

# import pytest


def test_is_valid(cfg_folder):

    f = TM1CfgFile(Path.joinpath(cfg_folder, "non_existent.cfg"))

    assert not f.is_valid()

    f = TM1CfgFile(Path.joinpath(cfg_folder, "minimal.cfg"))

    assert f.is_valid()


def test_read_and_write(test_folder):

    f = TM1CfgFile(Path.joinpath(test_folder, "tm1s.cfg"))

    # need to create the section
    f.config.add_section(f._section)

    param = "IntegratedSecurityMode"

    assert f.get_parameter(param) is None

    value = "1"

    f.set_parameter(param, value)

    assert f.get_parameter(param) == value

    # also re-open file to check it's been written to disk

    f2 = TM1CfgFile(Path.joinpath(test_folder, "tm1s.cfg"))

    assert f2.get_parameter(param) == value
