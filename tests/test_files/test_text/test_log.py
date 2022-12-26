from pathlib import Path

from tm1filetools.files import TM1ChangeLogFile, TM1LogFile, TM1ProcessErorrLogFile


def test_init(test_folder):

    f = TM1LogFile(Path.joinpath(test_folder, "tm1s.log"))

    assert f
    assert f.suffix == "log"


def test_changelog(test_folder):

    f = TM1ChangeLogFile(Path.joinpath(test_folder, "tm1s20200801080426.log"))

    assert f
    assert f.suffix == "log"

    assert f.exists

    log_rows = 0
    for row in f.reader():
        print(row[0])
        log_rows = log_rows + 1

    assert log_rows > 0
    assert log_rows == 3


def test_process_error_log(test_folder):

    f = TM1ProcessErorrLogFile(Path.joinpath(test_folder, "tm1processerror_23984572903485_myprocee_ss.log"))

    assert f
    assert f.suffix == "log"
    assert f.prefix.lower() == "tm1processerror_"
    assert f.process.lower() == "myprocee_ss"
