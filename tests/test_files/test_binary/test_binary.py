from pathlib import Path

from tm1filetools.files.binary.binary import TM1BinaryFile


def test_init(test_folder):

    f = TM1BinaryFile(Path.joinpath(test_folder, "cat.cub"))

    assert f
