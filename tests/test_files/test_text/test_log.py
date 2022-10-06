from pathlib import Path

from tm1filetools.files import TM1LogFile


def test_init(test_folder):

    f = TM1LogFile(Path.joinpath(test_folder, "tm1s.log"))

    assert f
    assert f.suffix == "log"
