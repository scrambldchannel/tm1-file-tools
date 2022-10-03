from pathlib import Path

from tm1filetools.files import TM1DimensionFile


def test_init(test_folder):

    f = TM1DimensionFile(Path.joinpath(test_folder, "koala.dim"))

    assert f
