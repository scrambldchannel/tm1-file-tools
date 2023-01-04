import sys
from pathlib import Path

import pytest

from tm1filetools.files import TM1CfgFile
from tm1filetools.tools.cfgfiletool import TM1CfgFileTool


def test_get_config_file(test_folder):

    ft = TM1CfgFileTool(path=test_folder)

    assert not ft.config_file

    f = test_folder / "tm1s.cfg"
    f.touch()

    ft = TM1CfgFileTool(path=test_folder)

    assert ft.config_file

    assert isinstance(ft.config_file, TM1CfgFile)


def test_get_paths_no_cfg(test_folder):

    ft = TM1CfgFileTool(path=test_folder)

    assert ft._get_data_path_param() is None
    assert ft.get_log_path() is None


def test_get_data_path_valid_cfg(cfg_folder):

    ft = TM1CfgFileTool(path=Path.joinpath(cfg_folder, "minimal"))

    assert ft.get_data_path()


def test_get_log_path_invalid_cfg(cfg_folder):

    ft = TM1CfgFileTool(Path.joinpath(cfg_folder, "invalid"))

    assert ft.get_log_path() is None


def test_get_data_path_local(cfg_folder):

    # the constructor requires a concrete path
    # which I can't find a way to instantiate cross platform
    if not sys.platform.startswith("win"):
        pytest.skip("skipping windows-only tests")

    # an absolute path is only going to get returned running locally
    ft = TM1CfgFileTool(path=Path.joinpath(cfg_folder, "abs_paths"), local=True)

    assert ft.get_data_path().is_absolute()

    ft = TM1CfgFileTool(path=Path.joinpath(cfg_folder, "rel_paths"), local=True)

    assert ft.get_data_path().exists
    assert ft.get_data_path().root == "\\"
    assert ft.get_data_path().stem == "data"


def test_get_log_path_local(cfg_folder):

    # the constructor requires a concrete path
    # which I can't find a way to instantiate cross platform
    if not sys.platform.startswith("win"):
        pytest.skip("skipping windows-only tests")

    # an absolute path is only going to get returned running locally
    ft = TM1CfgFileTool(path=Path.joinpath(cfg_folder, "abs_paths"), local=True)

    assert ft.get_log_path().is_absolute()

    ft = TM1CfgFileTool(path=Path.joinpath(cfg_folder, "rel_paths"), local=True)

    assert ft.get_log_path().exists
    assert ft.get_log_path().root == "\\"
    assert ft.get_log_path().stem == "logs"


def test_get_data_path_rel(cfg_folder):

    ft = TM1CfgFileTool(path=Path.joinpath(cfg_folder, "rel_paths"))

    assert ft

    assert ft.get_data_path()
    assert ft.get_data_path().is_absolute()


def test_get_log_path_rel(cfg_folder):

    ft = TM1CfgFileTool(path=Path.joinpath(cfg_folder, "rel_paths"))

    assert ft
    assert ft.get_data_path()
    assert ft.get_log_path().is_absolute()
