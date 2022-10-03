from pathlib import Path

from tm1filetools.files.binary.cube import (
    TM1AttributeCubeFile,
    TM1CellSecurityCubeFile,
    TM1CubeFile,
    TM1PicklistCubeFile,
)


def test_cube(test_folder):

    f = TM1CubeFile(Path.joinpath(test_folder, "cat.cub"))

    assert f


def test_attr_cube(test_folder):

    f = TM1CubeFile(Path.joinpath(test_folder, f"{TM1AttributeCubeFile.prefix}cat.cub"))

    assert f


def test_cellsec_cube(test_folder):

    f = TM1CubeFile(Path.joinpath(test_folder, f"{TM1CellSecurityCubeFile.prefix}cat.cub"))

    assert f


def test_picklist_cube(test_folder):

    f = TM1CubeFile(Path.joinpath(test_folder, f"{TM1PicklistCubeFile.prefix}cat.cub"))

    assert f
