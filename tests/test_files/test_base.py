from pathlib import Path

from tm1filetools.files.base import TM1File


def test_exists(test_folder):

    f = TM1File(Path.joinpath(test_folder, "cat.cub"))

    assert f.exists()

    f = TM1File(Path.joinpath(test_folder, "unicorn.cub"))

    assert not f.exists()


def test_delete(test_folder):

    f = TM1File(Path.joinpath(test_folder, "cat.cub"))

    assert f.exists()

    f.delete()

    assert not f.exists()


def test_rename(test_folder):

    f = TM1File(Path.joinpath(test_folder, "cat.cub"))

    assert f.exists()

    f.rename("bunyip")

    assert f.exists()

    assert not f.prefix
    assert f.is_tm1_file
    assert f.suffix == "cub"
    assert f.stem == "bunyip"


def test_name(test_folder):

    f = TM1File(Path.joinpath(test_folder, "cat.cub"))

    assert f.name == "cat.cub"


def test_stem(test_folder):

    f = TM1File(Path.joinpath(test_folder, "cat.cub"))

    assert f.stem == "cat"


def test_suffix(test_folder):

    f = TM1File(Path.joinpath(test_folder, "cat.cub"))

    assert f.suffix == "cub"


def test_is_control(test_folder):

    f = TM1File(Path.joinpath(test_folder, "cat.cub"))

    assert not f.is_control

    f = TM1File(Path.joinpath(test_folder, "}ElementAttributes_koala.cub"))

    assert f.is_control


def test_is_tm1_file(test_folder):

    f = TM1File(Path.joinpath(test_folder, "cat.cub"))
    assert f.is_tm1_file


def test_get_suffix_permutations(test_folder):

    f = TM1File(Path.joinpath(test_folder, "dog.ruX"))

    permutations = f._get_suffix_permutations()

    assert set(permutations) == set(["rux", "Rux", "RUx", "RUX", "rUx", "RuX", "rUX", "ruX"])
