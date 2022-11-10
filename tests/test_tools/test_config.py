import sys

import pytest

from tm1filetools.files import TM1CfgFile
from tm1filetools.tools.cfgfiletool import TM1CfgFileTool


def test_get_config_file(test_folder, empty_folder):

    ft = TM1CfgFileTool(path=empty_folder)

    assert not ft.config_file

    ft = TM1CfgFileTool(path=test_folder)

    assert ft.config_file

    assert isinstance(ft.config_file, TM1CfgFile)


def test_get_data_path_no_cfg(empty_folder):

    # if config file not found, should just be the original path
    ft = TM1CfgFileTool(path=empty_folder)

    assert ft.get_data_path() is None


def test_get_log_path_no_cfg(empty_folder):

    # if config file not found, should just be the original path
    ft = TM1CfgFileTool(path=empty_folder)

    assert ft.get_log_path() is None


def test_get_data_path_invalid_cfg(invalid_config_folder):

    ft = TM1CfgFileTool(path=invalid_config_folder)

    assert ft.get_data_path() is None


def test_get_log_path_invalid_cfg(invalid_config_folder):

    ft = TM1CfgFileTool(path=invalid_config_folder)

    assert ft.get_log_path() is None


def test_get_data_path_local(abs_config_folder, rel_config_folder):

    # the constructor requires a concrete path
    # which I can't find a way to instantiate cross platform
    if not sys.platform.startswith("win"):
        pytest.skip("skipping windows-only tests")

    # an absolute path is only going to get returned running locally
    ft = TM1CfgFileTool(path=abs_config_folder, local=True)

    assert ft.get_data_path().is_absolute()

    ft = TM1CfgFileTool(path=rel_config_folder, local=True)
    assert ft.get_data_path().exists
    assert ft.get_data_path().root == "\\"
    assert ft.get_data_path().stem == "data"


def test_get_log_path_local(abs_config_folder, rel_config_folder):

    # the constructor requires a concrete path
    # which I can't find a way to instantiate cross platform
    if not sys.platform.startswith("win"):
        pytest.skip("skipping windows-only tests")

    # an absolute path is only going to get returned running locally
    ft = TM1CfgFileTool(path=abs_config_folder, local=True)

    assert ft.get_log_path().is_absolute()

    ft = TM1CfgFileTool(path=rel_config_folder, local=True)
    assert ft.get_log_path().exists
    assert ft.get_log_path().root == "\\"
    assert ft.get_log_path().stem == "logs"


@pytest.mark.skip("failing")
def test_get_data_path_rel(rel_config_folder):

    ft = TM1CfgFileTool(path=rel_config_folder)

    assert ft.get_data_path()
    assert ft.get_data_path().exists()

    assert ft.get_data_path().is_absolute()


@pytest.mark.skip("failing")
def test_get_log_path_rel(rel_config_folder):

    ft = TM1CfgFileTool(path=rel_config_folder)

    assert ft.get_log_path().exists()
    assert ft.get_log_path().is_absolute()
