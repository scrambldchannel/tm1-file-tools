from pathlib import Path

from tm1filetools.files import TM1ProcessFile


def test_init(test_folder):

    p = TM1ProcessFile(Path.joinpath(test_folder, "copy data from my cube.pro"))

    assert p
    assert p.suffix == "pro"
