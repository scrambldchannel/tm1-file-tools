from pathlib import Path

from tm1filetools.files.text.cma import TM1CMAFile


def test_get_delimiter(test_folder):

    f = TM1CMAFile(Path.joinpath(test_folder, "test.cma"))

    assert not f._get_delimiter()
    assert not f.delimiter

    # should we make this a method?
    f._path.touch()

    f.write('"Sales Planning","202301","Software","Germany",1000000')

    assert f._get_delimiter() == ","
    assert f.delimiter


def test_get_cube(test_folder):

    f = TM1CMAFile(Path.joinpath(test_folder, "test.cma"))

    assert not f._get_cube()
    assert not f.cube

    # should we make this a method?
    f._path.touch()

    f.write('"Sales Planning","202301","Software","Germany",1000000')

    assert f._get_cube() == "Sales Planning"
    assert f.cube == "Sales Planning"
