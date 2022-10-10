from pathlib import Path

from tm1filetools.files import TM1DimensionFile


def test_init(test_folder):

    f = TM1DimensionFile(Path.joinpath(test_folder, "koala.dim"))

    assert f
    assert f.suffix == "dim"

    f = TM1DimensionFile(Path.joinpath(test_folder, "wallaby.DIM"))

    assert f
    assert f.suffix == "DIM"
