from pathlib import Path

from tm1filetools.files.text.cma import TM1CMAFile


def test_get_delimiter(export_folder):

    f = TM1CMAFile(Path.joinpath(export_folder, "nofile.cma"))

    assert not f._get_delimiter()
    assert not f.delimiter

    f = TM1CMAFile(Path.joinpath(export_folder, "Sales_2022.cma"))

    assert f._get_delimiter() == ","


def test_get_cube(export_folder):

    f = TM1CMAFile(Path.joinpath(export_folder, "test.cma"))

    assert not f._get_cube()
    assert not f.cube

    f = TM1CMAFile(Path.joinpath(export_folder, "Sales_2022.cma"))
    assert f._get_cube() == "Sales"


def test_reader(export_folder):

    f = TM1CMAFile(Path.joinpath(export_folder, "Sales_2022.cma"))

    row = next(f.reader())

    assert row.val_n == 200
    assert not row.val_s


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


def test_el_filter(export_folder):

    el_str = ":202301"

    f = TM1CMAFile(Path.joinpath(export_folder, "Sales_2022.cma"))

    rows = []
    for row in f.reader(el_filter=el_str):

        rows.append(row)

    assert len(rows) == 0

    el_str = ":202203"

    rows = []
    for row in f.reader(el_filter=el_str):

        rows.append(row)

    assert len(rows) == 2

    el_str = ":202203:::Comment"

    rows = []
    for row in f.reader(el_filter=el_str):

        rows.append(row)

    assert len(rows) == 1
