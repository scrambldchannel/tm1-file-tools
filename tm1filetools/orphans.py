# from typing import List

# from .general import get_cub_files, get_dim_files, get_files_by_ext, get_rux_files
# from .tools.filetool import TM1FileTool


# def get_orphan_attribute_files(path: str, ext: str, strip_prefix=False) -> List[str]:
#     """
#     Returns a list of orphaned attributes files (e.g. an attribute dim or cube for a dim that doesn't exist)
#     """

#     # get a list of all the dimension files
#     dims = get_dim_files(path)

#     artifacts = get_files_by_ext(path=path, ext=ext, prefix=TM1FileTool.attr_prefix)

#     orphans = []

#     for a in artifacts:

#         # python 3.9 dependent
#         a_dim = a.removeprefix(TM1FileTool.attr_prefix)

#         if a_dim not in dims:

#             if strip_prefix:
#                 orphans.append(a_dim)
#             else:
#                 orphans.append(a)

#     return orphans


# def get_orphan_attribute_cube_files(path: str, strip_prefix=False) -> List[str]:
#     """
#     Returns a list of orphaned attribute cubes
#     """

#     return get_orphan_attribute_files(path=path, ext="cub", strip_prefix=strip_prefix)


# def get_orphan_attribute_dim_files(path: str, strip_prefix=False) -> List[str]:
#     """
#     Returns a list of orphaned attribute dimensions
#     """

#     return get_orphan_attribute_files(path=path, ext="dim", strip_prefix=strip_prefix)
