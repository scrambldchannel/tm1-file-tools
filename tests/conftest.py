import pytest

from tm1filetools.files.general import attr_prefix

cub_files = ["cat", "dog"]
rux_files = ["dog", "giraffe"]
dim_files = ["koala", "possum"]
blb_files = ["emu", "unicorn"]
dim_attributes = ["koala", "kangaroo"]
cub_attributes = ["koala", "humphrey"]


@pytest.fixture(scope="session")
def artifact_files(tmp_path_factory):
    """
    Create a bunch of temp files that can be used to test the filesys functions with session scope
    """

    # create a temp path
    d = tmp_path_factory.mktemp("data")

    # create the temp files

    for c in cub_files:

        f = d / f"{c}.cub"
        f.touch()

    for r in rux_files:

        f = d / f"{r}.rux"
        f.touch()

    for df in dim_files:

        f = d / f"{df}.dim"
        f.touch()

    for b in blb_files:

        f = d / f"{b}.blb"
        f.touch()

    for da in dim_attributes:

        da = attr_prefix + da

        f = d / f"{da}.dim"
        f.touch()

    for ca in cub_attributes:

        ca = attr_prefix + ca

        f = d / f"{ca}.cub"
        f.touch()

    # return the path
    return d


@pytest.fixture(scope="module")
def artifact_files_mixed_case(tmp_path_factory):
    """
    Create a bunch of temp files that can be used to test the filesys functions with session scope
    """

    # create a temp path
    d = tmp_path_factory.mktemp("data")

    # create the temp files
    # There is probably a slicker way of doing this but this covers the main use case
    for c in cub_files:

        f = d / f"{c}.cub"
        f.touch()

    for r in rux_files:

        f = d / f"{r}.RUX"
        f.touch()

    for df in dim_files:

        f = d / f"{df}.dIm"
        f.touch()

    for b in blb_files:

        f = d / f"{b}.bLB"
        f.touch()

    for da in dim_attributes:

        da = attr_prefix + da
        f = d / f"{da}.DIM"
        f.touch()

    for ca in cub_attributes:

        ca = attr_prefix + ca

        f = d / f"{ca}.CUB"
        f.touch()

    # return the path
    return d
