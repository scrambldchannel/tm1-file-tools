# import pytest

# from tm1filetools.tools.filetool import TM1FileTool


# def test_orphan_ruxes(tm1_file_tool_test):

#     orphans = tm1_file_tool_test.get_orphan_ruxes()

#     assert orphans.count("foo") == 0
#     assert orphans.count("giraffe") == 1


# def test_orphan_attr_dims(tm1_file_tool_test, tm1_file_tool_test_mixed_case):

#     orphans = tm1_file_tool_test.get_orphan_attr_dims()

#     assert len(orphans) > 0
#     assert orphans.count("koala") == 0
#     assert orphans.count("kangaroo") == 1

#     # orphans = tm1_file_tool_test_mixed_case.get_orphan_attr_dims()

#     # assert len(orphans) > 0

#     # assert orphans.count(f"{TM1FileTool.attr_prefix}koala") == 0

#     # assert orphans.count(f"{TM1FileTool.attr_prefix}kangaroo") == 1


# # def test_orphan_attr_cube(artifact_files):

# #     orphans = get_orphan_attribute_cube_files(artifact_files, strip_prefix=True)

# #     assert len(orphans) > 0

# #     assert orphans.count("foo") == 0

# #     assert orphans.count("humphrey") == 1

# #     orphans = get_orphan_attribute_cube_files(artifact_files)

# #     assert len(orphans) > 0

# #     assert orphans.count(TM1FileTool.attr_prefix + "foo") == 0

# #     assert orphans.count(TM1FileTool.attr_prefix + "humphrey") == 1
