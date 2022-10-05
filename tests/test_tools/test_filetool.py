# import pytest

from tm1filetools.files.text.cfg import TM1CfgFile
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


def test_get_data_path_abs(abs_config_folder):

    # an absolute path is only going to get returned running locally
    ft = TM1FileTool(path=abs_config_folder, local=True)

    assert ft.data_path.is_absolute()


def test_get_data_path_rel(rel_config_folder):

    ft = TM1FileTool(path=rel_config_folder)

    assert ft.data_path.is_absolute()
    assert ft.data_path.exists()


# def test_get_blbs(tm1_file_tool_test, tm1_file_tool_test_mixed_case):

#     blbs = tm1_file_tool_test.get_blbs()

#     assert blbs.count("foo") == 0
#     assert blbs.count("emu") == 1

#     blbs = tm1_file_tool_test_mixed_case.get_blbs()

#     assert blbs.count("foo") == 0
#     assert blbs.count("emu") == 1


# def test_get_rux(tm1_file_tool_test, tm1_file_tool_test_mixed_case):

#     ruxes = tm1_file_tool_test.get_ruxes()

#     assert ruxes.count("cockatoo") == 0
#     assert ruxes.count("giraffe") == 1

#     ruxes = tm1_file_tool_test_mixed_case.get_ruxes()

#     assert ruxes.count("cockatoo") == 0
#     assert ruxes.count("giraffe") == 1


# def test_get_dims(tm1_file_tool_test, tm1_file_tool_test_mixed_case):

#     dims = tm1_file_tool_test.get_dims()

#     assert dims.count("bunyip") == 0
#     assert dims.count("possum") == 1

#     dims = tm1_file_tool_test_mixed_case.get_dims()

#     assert dims.count("bunyip") == 0
#     assert dims.count("possum") == 1


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


# def test_get_attribute_cubes(tm1_file_tool_test, tm1_file_tool_test_mixed_case):

#     attr_cubs = tm1_file_tool_test.get_attr_cubs()

#     assert attr_cubs.count(TM1FileTool.attr_prefix + "cockatoo") == 0
#     assert attr_cubs.count(TM1FileTool.attr_prefix + "humphrey") == 1

#     attr_cubs = tm1_file_tool_test_mixed_case.get_attr_cubs()

#     assert attr_cubs.count(TM1FileTool.attr_prefix + "cockatoo") == 0
#     assert attr_cubs.count(TM1FileTool.attr_prefix + "humphrey") == 1
