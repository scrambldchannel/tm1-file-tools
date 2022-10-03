from pathlib import Path

from tm1filetools.files.binary.cube import TM1CubeFile


def test_init(test_folder):

    f = TM1CubeFile(Path.joinpath(test_folder, "cat.cub"))

    assert f
