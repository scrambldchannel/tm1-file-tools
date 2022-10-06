# import pytest

from tm1filetools.files import TM1AttributeDimensionFile
from tm1filetools.tools import TM1FileTool


def test_get_model_dims(test_folder):

    ft = TM1FileTool(test_folder)

    dims = ft.get_model_dimensions()

    assert any(d.stem == "koala" for d in dims)
    assert all(d.stem != f"{TM1AttributeDimensionFile.prefix}koala" for d in dims)


def test_get_control_dims(test_folder):

    ft = TM1FileTool(test_folder)

    dims = ft.get_control_dimensions()

    assert any(d.stem == f"{TM1AttributeDimensionFile.prefix}koala" for d in dims)
    assert all(d.stem != "koala" for d in dims)


# def test_get_attr_dims(test_folder):

#     ft = TM1FileTool(test_folder)

#     dims = ft.get_attr_dimensions()

# assert any(d.stem == f"{TM1AttributeDimensionFile.prefix}koala" for d in dims)
# assert any(d.stem == f"{TM1AttributeDimensionFile.prefix}unicorn" for d in dims)
# assert all(d.stem != "koala" for d in dims)


# def test_find_cubes(test_folder):

#     ft = TM1FileTool(test_folder)

#     cubes = ft._find_cubes()

#     assert cubes

#     assert any(c.stem == "cat" for c in cubes)
#     assert all(c.stem != "unicorn" for c in cubes)


# def test_find_rules(test_folder):

#     ft = TM1FileTool(test_folder)

#     rules = ft._find_rules()

#     assert rules

#     assert any(r.stem == "dog" for r in rules)
#     assert all(r.stem != "basilisk" for r in rules)


# def test_find_subs(test_folder):

#     ft = TM1FileTool(test_folder)

#     subs = ft._find_subs()

#     assert subs

#     assert any(r.stem == "platypus" for r in subs)
#     assert all(r.stem != "womble" for r in subs)


# # def test_get_attribute_dims(test_folder):

# #     ft = TM1FileTool(test_folder)

# #     attr_dims = ft._find_attr_dims()

# # assert attr_dims

# # assert any(r.stem == "kangaroo" for r in subs)
# # assert all(r.stem != "cockatoo" for r in subs)


# # def test_get_blbs(tm1_file_tool_test, tm1_file_tool_test_mixed_case):

# #     blbs = tm1_file_tool_test.get_blbs()

# #     assert blbs.count("foo") == 0
# #     assert blbs.count("emu") == 1

# #     blbs = tm1_file_tool_test_mixed_case.get_blbs()

# #     assert blbs.count("foo") == 0
# #     assert blbs.count("emu") == 1

# # def test_get_attribute_cubes(tm1_file_tool_test, tm1_file_tool_test_mixed_case):

# #     attr_cubs = tm1_file_tool_test.get_attr_cubs()

# #     assert attr_cubs.count(TM1FileTool.attr_prefix + "cockatoo") == 0
# #     assert attr_cubs.count(TM1FileTool.attr_prefix + "humphrey") == 1

# #     attr_cubs = tm1_file_tool_test_mixed_case.get_attr_cubs()

# #     assert attr_cubs.count(TM1FileTool.attr_prefix + "cockatoo") == 0
# #     assert attr_cubs.count(TM1FileTool.attr_prefix + "humphrey") == 1
