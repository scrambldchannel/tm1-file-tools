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


def test_name(test_folder):

    f = TM1File(Path.joinpath(test_folder, "cat.cub"))

    assert f.name == "cat.cub"


def test_stem(test_folder):

    f = TM1File(Path.joinpath(test_folder, "cat.cub"))

    assert f.stem == "cat"


def test_prefix(test_folder):

    f = TM1File(Path.joinpath(test_folder, "cat.cub"))

    assert f.prefix is None

    f = TM1File(Path.joinpath(test_folder, "}ElementAttributes_cat.cub"))

    assert f.prefix == f.prefixes["attr_prefix"]


def test_suffix(test_folder):

    f = TM1File(Path.joinpath(test_folder, "cat.cub"))

    assert f.suffix == "cub"


def test_is_control(test_folder):

    f = TM1File(Path.joinpath(test_folder, "cat.cub"))

    assert not f.is_control_object()

    f = TM1File(Path.joinpath(test_folder, "}ElementAttributes_koala.cub"))

    assert f.is_control_object()


def test_is_tm1_file(test_folder):

    f = TM1File(Path.joinpath(test_folder, "cat.cub"))

    print(f.suffix)

    # print("cub" in f.suffixes.values())
    assert f.is_tm1_file()

    f = TM1File(Path.joinpath(test_folder, "unicorn.txt"))

    assert not f.is_tm1_file()
