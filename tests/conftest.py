import pytest

from tm1filetools.files.binary.cube import TM1AttributeCubeFile
from tm1filetools.files.binary.dimension import TM1AttributeDimensionFile
from tm1filetools.files.text.subset import TM1SubsetFile
from tm1filetools.files.text.view import TM1ViewFile

dim_files = ["koala.DIM", "possum.dim"]
dim_attributes = ["koala.dim", "kangaroo.dim"]
cub_files = ["cat.cub", "dog.CUB"]
cub_attributes = ["koala.cub", "humphrey.CUB"]
rux_files = ["dog.ruX", "giraffe.rux", "rux_1.rux"]
process_files = ["dingo.PRO", "wombat.pro", "}fraggle.pRO"]
cho_files = ["quokka.cho", "black_SNAKE.cho", "}brown_snake.cHO"]
sub_files = ["platypus.sub", "donkey.SUB", "}dolphin.suB"]
sub_folders = ["cat", "koala"]
view_files = ["mouse.vue", "squirrel.VUE", "}shark.vue"]
view_folders = ["cat", "koala"]
feeders_files = ["cat.feeders", "possum.FEEDERS"]
# should also add in a TI process error log
# I am unsure about how the process error string should look exactly
log_files = ["tm1s.log", "tm1server.LOG", "TM1ProcessError_123123_myproc.log"]
blb_files = ["emu.blb", "unicorn.blb"]
cma_files = ["bunyip.CMA", "troll.cma"]
junk_files = ["cat.cub.bak", "no_extension", "zzzBackup12.zip"]


@pytest.fixture(scope="function")
def empty_folder(tmp_path_factory):
    """
    Create an empty folder for testing
    """

    return tmp_path_factory.mktemp("data")


@pytest.fixture(scope="function")
def invalid_config_folder(tmp_path_factory):
    """
    Create a folder with an invalid config file
    """

    d = tmp_path_factory.mktemp("data")

    f = d / "tm1s.cfg"
    f.write_text("[NOSECTION]")

    return d


@pytest.fixture(scope="function")
def abs_config_folder(tmp_path_factory):
    """
    Create a folder with an absolute path
    """

    d = tmp_path_factory.mktemp("data")

    f = d / "tm1s.cfg"

    cfg = r"""[TM1S]
    DataBaseDirectory = c:\TM1\data
    LoggingDirectory = c:\TM1\logs
    """

    f.write_text(cfg)

    # also create the data

    return d


@pytest.fixture(scope="function")
def rel_config_folder(tmp_path_factory):
    """
    Create a folder with an absolute path
    """

    d = tmp_path_factory.mktemp("data")

    f = d / "tm1s.cfg"

    # still don't think this is working...

    cfg = r"""[TM1S]
    DataBaseDirectory = .\data
    LoggingDirectory = .\logs

    """

    f.write_text(cfg)

    # also create the directories
    data_dir = d / "data"
    data_dir.mkdir()

    log_dir = d / "logs"
    log_dir.mkdir()

    for log in log_files:
        f = log_dir / f"{log}"
        f.touch()

    return d


@pytest.fixture(scope="function")
def test_folder(tmp_path_factory):
    """
    Create a bunch of temp files that can be used to test the filesys functions with session scope
    """

    # create a temp path
    d = tmp_path_factory.mktemp("data")

    # create cfg file

    f = d / "tm1s.cfg"
    f.touch()

    # create the temp files

    for c in cub_files:

        f = d / f"{c}"
        f.touch()

    for r in rux_files:

        f = d / f"{r}"
        f.touch()

    # add sample ruxes
    rux_1 = r"""

Skipcheck ;

[] = STET;
FEEDERS    ;
"""
    f = d / "rux_1.ruX"

    f.write_text(rux_1)

    for df in dim_files:

        f = d / f"{df}"
        f.touch()

    for b in blb_files:

        f = d / f"{b}"
        f.touch()

    for c in cma_files:

        f = d / f"{c}"
        f.touch()

    # add sample cma
    cma = r""""Planning:Sales",","BP","202201","Sales","Australia","Amount",200
Planning:Sales",","BP","202202","Sales","Australia","Amount",300
Planning:Sales",","BP","202203","Sales","Australia","Amount",500
Planning:Sales",","BP","202203","Sales","Australia","Comment","To the moon!"
"""
    f = d / "Sales.cma"

    f.write_text(cma)

    for fd in feeders_files:

        f = d / f"{fd}"
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

    for j in junk_files:

        f = d / j
        f.touch()

    for p in process_files:

        f = d / f"{p}"
        f.touch()

    for c in cho_files:

        f = d / f"{c}"
        f.touch()

    for lg in log_files:

        f = d / f"{lg}"
        f.touch()

    # add a basic transaction log for testing
    changelog = r""" #LOG_FORMAT=1
#LOGID=6
#LOGIV=
"","20200801185011","20200801185011","Admin","S","20200722131536","20200801185011","}DimensionProperties","}dimensions","LAST_TIME_UPDATED",""
#"","20200802084038","CubeSerialized: TM1py_tests_annotations: by Admin"
"","20200802084728","20200802084728","Admin","N","0","6","TM1py_Tests_Cell_Cube_RPS1","e2","e3",""

"""

    f = d / "tm1s20200801080426.log"

    f.write_text(changelog)

    # return the path
    return d
