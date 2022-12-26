from pathlib import Path

from tm1filetools.files.text.cma import TM1CMAFile


def test_get_delimiter(test_folder):

    f = TM1CMAFile(Path.joinpath(test_folder, "test.cma"))

    assert not f._get_delimiter()
    assert not f.delimiter

    f._path.touch()

    f.write('"Planning:Sales Planning","202301","Software","Germany",1000000')

    assert f._get_delimiter() == ","
    assert not f.delimiter


def test_get_cube(test_folder):

    f = TM1CMAFile(Path.joinpath(test_folder, "test.cma"))

    assert not f._get_cube()
    assert not f.cube

    f._path.touch()

    f.write('"Planning:Sales Planning","202301","Software","Germany",1000000')

    assert f._get_cube() == "Sales Planning"


def test_parse_els():

    el_str = "202301:Software:Germany"

    els = TM1CMAFile._parse_els(el_str)

    assert len(els) == 3

    assert els[0] == "202301"

    el_str = "202302:Hardware:Australia::"

    els = TM1CMAFile._parse_els(el_str)

    # two trailing els should have been dropped
    assert len(els) == 3

    assert els[1] == "Hardware"

    el_str = "202302:Hardware:Australia::Value"

    els = TM1CMAFile._parse_els(el_str)

    assert len(els) == 5

    # empty value should be retained to preserve index of value
    assert els[3] == ""
    assert els[4] == "Value"
