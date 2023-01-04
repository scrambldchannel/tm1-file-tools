from pathlib import Path

from tm1filetools.files import TM1TextFile


def test_read_and_write(empty_folder):

    # extension doesn't actually matter
    f = empty_folder / "emu.txt"
    f.touch()

    f = TM1TextFile(Path.joinpath(empty_folder, "emu.txt"))

    assert f.read() == ""

    f.write("some text")

    assert f.read() == "some text"


def test_is_non_empty(test_folder):

    f = TM1TextFile(Path.joinpath(test_folder, "emu.blb"))

    assert not f._get_non_empty()

    f.write("some text")

    assert f._get_non_empty()
    assert f.is_non_empty
