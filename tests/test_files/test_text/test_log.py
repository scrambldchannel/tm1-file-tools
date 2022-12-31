from pathlib import Path

from tm1filetools.files import TM1ChangeLogFile, TM1LogFile, TM1ProcessErorrLogFile


def test_init(log_folder):

    f = TM1LogFile(Path.joinpath(log_folder, "tm1s.log"))

    assert f
    assert f.suffix == "log"


def test_changelog(log_folder):

    f = TM1ChangeLogFile(Path.joinpath(log_folder, "tm1s20200801080426.log"))

    assert f
    assert f.suffix == "log"

    assert f.exists

    log_rows = 0
    for row in f.reader():
        log_rows = log_rows + 1

    assert log_rows > 0
    assert log_rows == 1

    log_rows = 0
    for row in f.reader(control=True):
        log_rows = log_rows + 1

    assert log_rows > 0
    assert log_rows == 2


def test_changelog_cubes(log_folder):

    f = TM1ChangeLogFile(Path.joinpath(log_folder, "tm1s20200801080426.log"))

    assert f
    assert f.suffix == "log"

    assert f.exists

    cubes = f.get_cubes()
    assert cubes
    assert len(cubes) == 1

    assert "TM1py_Tests_Cell_Cube_RPS1" in cubes

    cubes = f.get_cubes(control=True)
    assert len(cubes) == 2
    assert "}DimensionProperties" in cubes


def test_changelog_users(log_folder):

    f = TM1ChangeLogFile(Path.joinpath(log_folder, "tm1s20200801080426.log"))

    assert f
    assert f.suffix == "log"

    assert f.exists

    users = f.get_users()
    assert users
    assert len(users) == 1


def test_process_error_log(log_folder):

    # we should get a sample of an actual error log and use for testing
    f = TM1ProcessErorrLogFile(Path.joinpath(log_folder, "tm1processerror_23984572903485_myprocee_ss.log"))

    assert f
    assert f.suffix == "log"
    assert f.prefix.lower() == "tm1processerror_"
    assert f.process.lower() == "myprocee_ss"
