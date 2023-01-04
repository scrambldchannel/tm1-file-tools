from pathlib import Path

import pytest

from tm1filetools.files.binary.cube import TM1AttributeCubeFile
from tm1filetools.files.binary.dimension import TM1AttributeDimensionFile
from tm1filetools.files.text.subset import TM1SubsetFile
from tm1filetools.files.text.view import TM1ViewFile

dim_files = ["koala.DIM", "possum.dim"]
dim_attributes = ["koala.dim", "kangaroo.dim"]
cub_files = ["cat.cub", "dog.CUB"]
cub_attributes = ["koala.cub", "humphrey.CUB"]
rux_files = ["dog.ruX", "giraffe.rux"]
sub_files = ["platypus.sub", "donkey.SUB", "}dolphin.suB"]
sub_folders = ["cat", "koala"]
view_files = ["mouse.vue", "squirrel.VUE", "}shark.vue"]
view_folders = ["cat", "koala"]


@pytest.fixture(scope="function")
def test_folder(tmp_path_factory):
    """
    Create a bunch of temp files that can be used to test the filesys functions with session scope
    """

    # create a temp path
    d = tmp_path_factory.mktemp("data")

    # create the temp files

    for c in cub_files:

        f = d / f"{c}"
        f.touch()

    for r in rux_files:

        f = d / f"{r}"
        f.touch()

    for df in dim_files:

        f = d / f"{df}"
        f.touch()

    # create dir for subsets

    user_dir = d / "Alex"
    user_dir.mkdir()

    for sf in sub_folders:

        subs_dir = d / f"{sf}{TM1SubsetFile.folder_suffix}"
        subs_dir.mkdir()
        # create dir for subsets

        user_subs_dir = user_dir / f"{sf}{TM1SubsetFile.folder_suffix}"
        user_subs_dir.mkdir()

        for s in sub_files:

            f = subs_dir / f"{s}"
            f.touch()

            f = user_subs_dir / f"{s}"
            f.touch()

    # create dir for private views
    user_dir = d / "Chimpy"
    user_dir.mkdir()

    for vf in view_folders:
        # create dir for views
        views_dir = d / f"{vf}{TM1ViewFile.folder_suffix}"
        views_dir.mkdir()
        user_views_dir = user_dir / f"{vf}{TM1ViewFile.folder_suffix}"
        user_views_dir.mkdir()

        for v in view_files:

            f = views_dir / f"{v}"
            f.touch()

            f = user_views_dir / f"{v}"
            f.touch()

    for da in dim_attributes:

        da = TM1AttributeDimensionFile.prefix + da

        f = d / f"{da}"
        f.touch()

    for ca in cub_attributes:

        ca = TM1AttributeCubeFile.prefix + ca

        f = d / f"{ca}"
        f.touch()

    return d


@pytest.fixture(scope="function")
def data_folder():

    path = Path.joinpath(Path.cwd(), "tests", "samples", "server", "data")

    return path


@pytest.fixture(scope="function")
def log_folder():

    path = Path.joinpath(Path.cwd(), "tests", "samples", "server", "logs")

    return path


@pytest.fixture(scope="function")
def export_folder():

    # this is an arbitrary folder for cmas
    path = Path.joinpath(Path.cwd(), "tests", "samples", "server", "exports")

    return path


@pytest.fixture(scope="function")
def cfg_folder():

    path = Path.joinpath(Path.cwd(), "tests", "samples", "config_files")

    return path


@pytest.fixture(scope="function")
def subset_json_out_folder():

    path = Path.joinpath(Path.cwd(), "tests", "samples", "json_out", "subsets")

    return path


@pytest.fixture(scope="function")
def view_json_out_folder():

    path = Path.joinpath(Path.cwd(), "tests", "samples", "json_out", "views")

    return path


@pytest.fixture(scope="function")
def proc_json_out_folder():

    path = Path.joinpath(Path.cwd(), "tests", "samples", "json_out", "procs")

    return path
