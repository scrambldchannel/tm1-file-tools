# from .helpers import get_name_part, case_insensitive_glob
from typing import List

from .general import (
    attr_prefix,
    get_cub_files,
    get_dim_files,
    get_files_by_ext,
    get_rux_files,
)


def get_orphan_rux_files(path: str) -> List[str]:
    """
    Returns a list of orphaned rux files (e.g. a rux file without a corresponding cube)
    """

    # how do I get case sensitivity to work here? Is there another library I should use instead?

    objects = get_cub_files(path)
    artifacts = get_rux_files(path)

    orphans = []

    for a in artifacts:

        if a not in objects:

            orphans.append(a)

    return orphans


def get_orphan_attribute_files(path: str, ext: str, strip_prefix=False) -> List[str]:
    """
    Returns a list of orphaned attributes files (e.g. an attribute dim or cube for a dim that doesn't exist)
    """

    # get a list of all the dimension files
    dims = get_dim_files(path)

    artifacts = get_files_by_ext(path=path, ext=ext, prefix=attr_prefix)

    orphans = []

    for a in artifacts:

        # python 3.9 dependent
        a_dim = a.removeprefix(attr_prefix)

        if a_dim not in dims:

            if strip_prefix:
                orphans.append(a_dim)
            else:
                orphans.append(a)

    return orphans


def get_orphan_attribute_cube_files(path: str, strip_prefix=False) -> List[str]:
    """
    Returns a list of orphaned attribute cubes
    """

    return get_orphan_attribute_files(path=path, ext="cub", strip_prefix=strip_prefix)


def get_orphan_attribute_dim_files(path: str, strip_prefix=False) -> List[str]:
    """
    Returns a list of orphaned attribute dimensions
    """

    return get_orphan_attribute_files(path=path, ext="dim", strip_prefix=strip_prefix)
