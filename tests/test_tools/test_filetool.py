# import pytest

# from tm1filetools.tools.filetool import TM1FileTool


# def test_case_insensitive_glob(test_tm1tool):

#     # this is lazy and isn't portable
#     # names = ["/random_folder/chimpy.RuX", "Trevor.blb", "julie.PRO"]

#     # struggling to know how to test this :shrug:

#     # result = TM1FileTool._case_insensitive_glob("RuX")

#     pytest.skip("no idea how to test this")
#     # assert result


# def test_get_files(test_tm1tool):

#     dims = test_tm1tool._get_files(ext="dim")

#     assert len(dims) > 0


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
