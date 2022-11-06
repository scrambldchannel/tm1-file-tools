from pathlib import Path

from tm1filetools.files import TM1ChoreFile


def test_init(test_folder):

    p = TM1ChoreFile(Path.joinpath(test_folder, "copy data from my cube.cho"))

    assert p
    assert p.suffix == "cho"
