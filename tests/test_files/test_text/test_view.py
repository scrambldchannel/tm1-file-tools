import itertools
import json
from pathlib import Path

import pytest

from tm1filetools.files import TM1ViewFile

sample_views = [
    "test.tm1filetools.static_view",
    "test.tm1filetools.static_view_with_named_title_subset",
]

mandatory_json_fields = [
    "Name",
    "Columns",
    "Rows",
    "Titles",
    "SuppressEmptyColumns",
    "SuppressEmptyRows",
    "FormatString",
]


@pytest.mark.parametrize("view,json_field", itertools.product(sample_views, mandatory_json_fields))
def test_json(data_folder, view_json_out_folder, view, json_field):

    v = TM1ViewFile(Path.joinpath(data_folder, f"{view}.vue"))

    assert v

    with open(Path.joinpath(view_json_out_folder, f"{view}.json"), "r") as f:
        expected_json_str = f.read()

    assert expected_json_str

    json_out = v._to_json()

    expected_json = json.loads(expected_json_str)

    # only name working for now
    if json_field != "Name":
        pytest.skip("Not yet implemented")

    assert json_out[json_field] == expected_json[json_field]


def test_public_view(test_folder):

    f = TM1ViewFile(Path.joinpath(test_folder, f"cat{TM1ViewFile.folder_suffix}", "squirrel.vue"))

    assert f.cube == "cat"
    assert f.stem == "squirrel"
    assert f.public
    assert f.owner is None


def test_private_view(test_folder):

    f = TM1ViewFile(
        Path.joinpath(test_folder, "Chimpy", f"cat{TM1ViewFile.folder_suffix}", "squirrel.vue"), public=False
    )

    assert f.cube == "cat"
    assert f.stem == "squirrel"
    assert not f.public
    assert f.owner == "Chimpy"


# this is kinda redundant as it's tested in test_public_view
def test_get_cube_name(test_folder):

    f = TM1ViewFile(Path.joinpath(test_folder, f"cat{TM1ViewFile.folder_suffix}", "squirrel.vue"))

    assert f._get_object_name() == "cat"


# this is kinda redundant as it's tested in test_private_view
def test_get_owner_name(test_folder):

    f = TM1ViewFile(
        Path.joinpath(test_folder, "Chimpy", f"cat{TM1ViewFile.folder_suffix}", "squirrel.vue"), public=False
    )

    assert f._get_owner_name() == "Chimpy"


def test_get_public_views_path(test_folder):

    f = TM1ViewFile(Path.joinpath(test_folder, f"cat{TM1ViewFile.folder_suffix}", "squirrel.VUE"))

    assert f._get_public_path() == Path.joinpath(test_folder, f"cat{TM1ViewFile.folder_suffix}")

    f = TM1ViewFile(
        Path.joinpath(test_folder, "Chimpy", f"cat{TM1ViewFile.folder_suffix}", "squirrel.VUE"), public=False
    )

    new_path = f._get_public_path()

    assert new_path == Path.joinpath(test_folder, f"cat{TM1ViewFile.folder_suffix}")


def test_move_to_public(test_folder):

    f = TM1ViewFile(
        Path.joinpath(test_folder, "Chimpy", f"cat{TM1ViewFile.folder_suffix}", "squirrel.VUE"), public=False
    )

    f.move_to_public()

    assert f._get_owner_name() is None
    assert f._path == Path.joinpath(test_folder, f"cat{TM1ViewFile.folder_suffix}", "squirrel.VUE")

    f = TM1ViewFile(Path.joinpath(test_folder, f"cat{TM1ViewFile.folder_suffix}", "squirrel.VUE"))

    assert f._get_owner_name() is None
    assert f._path == Path.joinpath(test_folder, f"cat{TM1ViewFile.folder_suffix}", "squirrel.VUE")
    assert f.public
