from pathlib import Path

from tm1filetools.files import TM1RulesFile


def test_init(test_folder):

    f = TM1RulesFile(Path.joinpath(test_folder, "dog.ruX"))

    assert f.stem == "dog"
    assert f.suffix == "ruX"


def test_feeders(data_folder):

    f = TM1RulesFile(Path.joinpath(data_folder, "skipcheck_feeders.rux"))

    assert f.has_feeders()


def test_skipcheck(data_folder):

    f = TM1RulesFile(Path.joinpath(data_folder, "skipcheck_feeders.rux"))

    assert f.has_skipcheck()
