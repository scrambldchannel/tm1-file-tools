import pytest

from tm1filetools.files.attribute_cube import TM1AttributeCubeFile
from tm1filetools.files.attribute_dimension import TM1AttributeDimensionFile
from tm1filetools.files.subset import TM1SubsetFile
from tm1filetools.files.view import TM1ViewFile

cub_files = ["cat", "dog"]
rux_files = ["dog", "giraffe"]
dim_files = ["koala", "possum"]
blb_files = ["emu", "unicorn"]
sub_files = ["platypus", "donkey"]
view_files = ["mouse", "squirrel"]
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

    # create dir for subsets
    subs_dir = d / f"cat{TM1SubsetFile.folder_suffix}"
    subs_dir.mkdir()
    # create dir for subsets
    user_dir = d / "Alex"
    user_dir.mkdir()
    user_subs_dir = user_dir / f"cat{TM1SubsetFile.folder_suffix}"
    user_subs_dir.mkdir()

    for s in sub_files:

        f = subs_dir / f"{s}.sub"
        f.touch()

        f = user_subs_dir / f"{s}.sub"
        f.touch()

    # create dir for views
    views_dir = d / f"cat{TM1ViewFile.folder_suffix}"
    views_dir.mkdir()
    # create dir for private views
    user_dir = d / "Chimpy"
    user_dir.mkdir()
    user_views_dir = user_dir / f"cat{TM1ViewFile.folder_suffix}"
    user_views_dir.mkdir()

    for v in view_files:

        f = views_dir / f"{v}.vue"
        f.touch()

        f = user_views_dir / f"{v}.vue"
        f.touch()

    for da in dim_attributes:

        da = TM1AttributeDimensionFile.prefix + da

        f = d / f"{da}.dim"
        f.touch()

    for ca in cub_attributes:

        ca = TM1AttributeCubeFile.prefix + ca

        f = d / f"{ca}.cub"
        f.touch()

    # return the path
    return d


# @pytest.fixture(scope="function")
# def test_tm1tool(test_folder):
#     # might want to change path to config file
#     return TM1FileTool(test_folder)
