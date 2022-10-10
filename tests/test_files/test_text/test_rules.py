from pathlib import Path

from tm1filetools.files import TM1RulesFile


def test_init(test_folder):

    f = TM1RulesFile(Path.joinpath(test_folder, "dog.ruX"))

    assert f.stem == "dog"
    assert f.suffix == "ruX"
