import pytest

from tm1filetools.tools.filetool import TM1FileTool

cub_files = ["cat", "dog"]
rux_files = ["dog", "giraffe"]
dim_files = ["koala", "possum"]
blb_files = ["emu", "unicorn"]
sub_files = ["platypus", "donkey"]
dim_attributes = ["koala", "kangaroo"]
cub_attributes = ["koala", "humphrey"]


@pytest.fixture(scope="function")
def test_folder(tmp_path_factory):
    """
    Create a bunch of temp files that can be used to test the filesys functions with session scope
    """

    # create a temp path
    d = tmp_path_factory.mktemp("data")

    # create cfg file

    f = d / "tm1.cfg"
    f.touch()

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

    for s in sub_files:

        f = d / f"{s}.sub"
        f.touch()

    for da in dim_attributes:

        da = TM1FileTool.attr_prefix + da

        f = d / f"{da}.dim"
        f.touch()

    for ca in cub_attributes:

        ca = TM1FileTool.attr_prefix + ca

        f = d / f"{ca}.cub"
        f.touch()

    # return the path
    return d
