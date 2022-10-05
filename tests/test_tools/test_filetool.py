import sys

import pytest

from tm1filetools.files import TM1CfgFile
from tm1filetools.tools.filetool import TM1FileTool


def test_case_insensitive_glob(test_folder):

    # pretty trivial tests but do seem to work
    # i.e. an empty list is false
    assert list(TM1FileTool._case_insensitive_glob(path=test_folder, pattern="tm1s.cfg"))
    assert not list(TM1FileTool._case_insensitive_glob(path=test_folder, pattern="THIS_FILE_DOES_NOT_EXIST"))
    assert list(TM1FileTool._case_insensitive_glob(path=test_folder, pattern="tm1s.CFG"))
    assert list(TM1FileTool._case_insensitive_glob(path=test_folder, pattern="TM1s.cFg"))


def test_get_config_file(test_folder, empty_folder):

    ft = TM1FileTool(path=empty_folder)

    assert not ft.config_file

    ft = TM1FileTool(path=test_folder)

    assert ft.config_file

    assert isinstance(ft.config_file, TM1CfgFile)


def test_get_data_path_no_cfg(empty_folder):

    # if config file not found, should just be the original path
    ft = TM1FileTool(path=empty_folder)

    assert ft.data_path == empty_folder


def test_get_data_path_invalid_cfg(invalid_config_folder):

    ft = TM1FileTool(path=invalid_config_folder)

    assert ft.data_path == invalid_config_folder


def test_get_data_path_local(abs_config_folder, rel_config_folder):

    # the constructor requires a concrete path
    # which I can't find a way to instantiate cross platform
    if not sys.platform.startswith("win"):
        pytest.skip("skipping windows-only tests")

    # an absolute path is only going to get returned running locally
    ft = TM1FileTool(path=abs_config_folder, local=True)

    assert ft.data_path.is_absolute()

    ft = TM1FileTool(path=rel_config_folder, local=True)

    assert not ft.data_path.is_absolute()


def test_get_data_path_rel(rel_config_folder):

    ft = TM1FileTool(path=rel_config_folder)

    assert ft.data_path.is_absolute()
    assert ft.data_path.exists()


def test_get_files_by_suffix(test_folder):

    ft = TM1FileTool(test_folder)

    dims = list(ft._get_files_by_suffix(suffix="dim"))

    assert dims

    exes = list(ft._get_files_by_suffix(suffix="exes"))

    assert not exes


def test_get_dims(test_folder):

    ft = TM1FileTool(test_folder)

    dims = ft._get_dims()

    assert dims

    assert any(d.stem == "koala" for d in dims)
    assert all(d.stem != "bunyip" for d in dims)


def test_get_cubes(test_folder):

    ft = TM1FileTool(test_folder)

    cubes = ft._get_cubes()

    assert cubes

    assert any(c.stem == "cat" for c in cubes)
    assert all(c.stem != "unicorn" for c in cubes)


def test_get_rules(test_folder):

    ft = TM1FileTool(test_folder)

    rules = ft._get_rules()

    assert rules

    assert any(r.stem == "dog" for r in rules)
    assert all(r.stem != "basilisk" for r in rules)


# def test_get_rux(tm1_file_tool_test, tm1_file_tool_test_mixed_case):

#     ruxes = tm1_file_tool_test.get_ruxes()

#     assert ruxes.count("cockatoo") == 0
#     assert ruxes.count("giraffe") == 1

#     ruxes = tm1_file_tool_test_mixed_case.get_ruxes()

#     assert ruxes.count("cockatoo") == 0
#     assert ruxes.count("giraffe") == 1


# def test_get_cubs(tm1_file_tool_test, tm1_file_tool_test_mixed_case):

#     cubs = tm1_file_tool_test.get_cubs()

#     assert cubs.count("basilisk") == 0
#     assert cubs.count("dog") == 1

#     cubs = tm1_file_tool_test_mixed_case.get_cubs()

#     assert cubs.count("basilisk") == 0
#     assert cubs.count("cat") == 1


# def test_get_subs(tm1_file_tool_test, tm1_file_tool_test_mixed_case):

#     subs = tm1_file_tool_test.get_subs()

#     assert subs.count("basilisk") == 0
#     assert subs.count("platypus") == 1

#     subs = tm1_file_tool_test_mixed_case.get_subs()

#     assert subs.count("basilisk") == 0
#     assert subs.count("platypus") == 1


# def test_get_attribute_dims(tm1_file_tool_test, tm1_file_tool_test_mixed_case):

#     attr_dims = tm1_file_tool_test.get_attr_dims()

#     assert attr_dims.count(TM1FileTool.attr_prefix + "cockatoo") == 0
#     assert attr_dims.count(TM1FileTool.attr_prefix + "kangaroo") == 1

#     attr_dims = tm1_file_tool_test_mixed_case.get_attr_dims()

#     assert attr_dims.count(TM1FileTool.attr_prefix + "cockatoo") == 0
#     assert attr_dims.count(TM1FileTool.attr_prefix + "kangaroo") == 1


# def test_get_blbs(tm1_file_tool_test, tm1_file_tool_test_mixed_case):

#     blbs = tm1_file_tool_test.get_blbs()

#     assert blbs.count("foo") == 0
#     assert blbs.count("emu") == 1

#     blbs = tm1_file_tool_test_mixed_case.get_blbs()

#     assert blbs.count("foo") == 0
#     assert blbs.count("emu") == 1

# def test_get_attribute_cubes(tm1_file_tool_test, tm1_file_tool_test_mixed_case):

#     attr_cubs = tm1_file_tool_test.get_attr_cubs()

#     assert attr_cubs.count(TM1FileTool.attr_prefix + "cockatoo") == 0
#     assert attr_cubs.count(TM1FileTool.attr_prefix + "humphrey") == 1

#     attr_cubs = tm1_file_tool_test_mixed_case.get_attr_cubs()

#     assert attr_cubs.count(TM1FileTool.attr_prefix + "cockatoo") == 0
#     assert attr_cubs.count(TM1FileTool.attr_prefix + "humphrey") == 1
