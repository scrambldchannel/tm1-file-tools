from pathlib import Path

from tm1filetools.files import TM1RulesFile


def test_init(test_folder):

    f = TM1RulesFile(Path.joinpath(test_folder, "dog.ruX"))

    assert f.stem == "dog"
    assert f.suffix == "ruX"


def test_feeders(test_folder):

    f = TM1RulesFile(Path.joinpath(test_folder, "rux_1.ruX"))

    feeders = f.has_feeders()
    assert feeders


def test_skipcheck(test_folder):

    f = TM1RulesFile(Path.joinpath(test_folder, "rux_1.ruX"))

    assert f.has_skipcheck()
