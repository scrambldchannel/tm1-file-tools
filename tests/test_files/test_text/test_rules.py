from pathlib import Path

from tm1filetools.files.text.rules import TM1RulesFile


def test_get_cube_path(test_folder):

    f = TM1RulesFile(Path.joinpath(test_folder, "dog.rux"))

    assert f._get_cube_path() == Path.joinpath(test_folder, "dog.cub")

    f = TM1RulesFile(Path.joinpath(test_folder, "giraffe.rux"))

    assert f._get_cube_path() == Path.joinpath(test_folder, "giraffe.cub")


def test_is_orphan(test_folder):

    f = TM1RulesFile(Path.joinpath(test_folder, "dog.rux"))

    assert not f.is_orphan()

    f = TM1RulesFile(Path.joinpath(test_folder, "giraffe.rux"))

    assert f.is_orphan()
