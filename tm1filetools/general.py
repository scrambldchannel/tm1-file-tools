from typing import List

from .helpers import case_insensitive_glob, get_name_part

# a bit ugly but :shrug:
attr_prefix = "}ElementAttributes_"
attr_prefix_lower = attr_prefix.lower()


def get_files_by_ext(path: str, ext: str, prefix: str = "", recursive: bool = False) -> List[str]:
    """
    Returns all files with specified ext and optional prefix
    """

    return [get_name_part(a) for a in case_insensitive_glob(f"{path}/{prefix}*.{ext}")]


def get_rux_files(path: str) -> List[str]:
    """
    Returns all rux files
    """

    return get_files_by_ext(path=path, ext="rux")


def get_cub_files(path: str) -> List[str]:
    """
    Returns all rux files
    """

    return get_files_by_ext(path=path, ext="cub")


def get_dim_files(path: str) -> List[str]:
    """
    Returns all dim files
    """

    return get_files_by_ext(path=path, ext="dim")


def get_attribute_dim_files(path: str, strip_prefix=False) -> List[str]:
    """
    Returns all attribute dim files
    """

    return get_files_by_ext(path=path, ext="dim", prefix=attr_prefix)


def get_attribute_cub_files(path: str, strip_prefix=False) -> List[str]:
    """
    Returns all attribute cub files
    """

    return get_files_by_ext(path=path, ext="cub", prefix=attr_prefix)


def get_attribute_rux_files(path: str) -> List[str]:
    """
    Returns all cub files
    """

    return get_files_by_ext(path=path, ext="cub", prefix=attr_prefix)


def get_blb_files(path: str) -> List[str]:
    """
    Returns all rux files
    """

    return get_files_by_ext(path=path, ext="blb")


def get_vue_files(path: str) -> List[str]:
    """
    Returns all vue files (i.e. views, nothing to do with vue.js)
    """

    return get_files_by_ext(path=path, ext="vue")


def get_sub_files(path: str) -> List[str]:
    """
    Returns all sub files
    """

    return get_files_by_ext(path=path, ext="sub")
