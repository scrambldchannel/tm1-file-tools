# import json
from pathlib import Path

from tm1filetools.files import TM1SubsetFile


def test_public_subset(test_folder):

    f = TM1SubsetFile(Path.joinpath(test_folder, f"cat{TM1SubsetFile.folder_suffix}", "platypus.sub"))

    assert f.dimension == "cat"
    assert f.stem == "platypus"
    assert f.public
    assert f.owner is None


def test_private_subset(test_folder):

    f = TM1SubsetFile(
        Path.joinpath(test_folder, "Alex", f"cat{TM1SubsetFile.folder_suffix}", "platypus.sub"), public=False
    )

    assert f.dimension == "cat"
    assert f.stem == "platypus"
    assert not f.public
    assert f.owner == "Alex"


# this is kinda redundant as it's tested in test_public_subset
def test_get_dimension_name(test_folder):

    f = TM1SubsetFile(Path.joinpath(test_folder, f"cat{TM1SubsetFile.folder_suffix}", "platypus.sub"))

    assert f._get_object_name() == "cat"


# this is kinda redundant as it's tested in test_private_subset
def test_get_owner_name(test_folder):

    f = TM1SubsetFile(
        Path.joinpath(test_folder, "Alex", f"cat{TM1SubsetFile.folder_suffix}", "platypus.sub"), public=False
    )

    assert f._get_owner_name() == "Alex"


def test_get_public_subsets_path(test_folder):

    f = TM1SubsetFile(Path.joinpath(test_folder, f"cat{TM1SubsetFile.folder_suffix}", "platypus.sub"))

    assert f._get_public_path() == Path.joinpath(test_folder, f"cat{TM1SubsetFile.folder_suffix}")

    f = TM1SubsetFile(
        Path.joinpath(test_folder, "Alex", f"cat{TM1SubsetFile.folder_suffix}", "platypus.sub"), public=False
    )

    new_path = f._get_public_path()

    assert new_path == Path.joinpath(test_folder, f"cat{TM1SubsetFile.folder_suffix}")


def test_move_to_public(test_folder):

    f = TM1SubsetFile(
        Path.joinpath(test_folder, "Alex", f"cat{TM1SubsetFile.folder_suffix}", "platypus.sub"), public=False
    )

    f.move_to_public()

    assert f._get_owner_name() is None
    assert f._path == Path.joinpath(test_folder, f"cat{TM1SubsetFile.folder_suffix}", "platypus.sub")

    f = TM1SubsetFile(Path.joinpath(test_folder, f"cat{TM1SubsetFile.folder_suffix}", "platypus.sub"))

    assert f._get_owner_name() is None
    assert f._path == Path.joinpath(test_folder, f"cat{TM1SubsetFile.folder_suffix}", "platypus.sub")
    assert f.public


def test_single_static_subset(json_dumps_folder):

    subset = "test.tm1filetools.single_element_static_subset"

    sub = TM1SubsetFile(Path.joinpath(json_dumps_folder, "subsets", f"{subset}.sub"))

    assert sub

    with open(Path.joinpath(json_dumps_folder, "subsets", f"{subset}.json"), "r") as f:
        expected_json_str = f.read()

    assert expected_json_str


def test_multi_static_subset(json_dumps_folder):

    subset = "test.tm1filetools.multi_element_static_subset"

    sub = TM1SubsetFile(Path.joinpath(json_dumps_folder, "subsets", f"{subset}.sub"))

    assert sub

    with open(Path.joinpath(json_dumps_folder, "subsets", f"{subset}.json"), "r") as f:
        expected_json_str = f.read()

    assert expected_json_str


def test_mdx_subset(json_dumps_folder):

    subset = "test.tm1filetools.mdx_subset"

    sub = TM1SubsetFile(Path.joinpath(json_dumps_folder, "subsets", f"{subset}.sub"))

    assert sub._get_mdx() == "{TM1SUBSETALL( [}Processes] )}"

    with open(Path.joinpath(json_dumps_folder, "subsets", f"{subset}.json"), "r") as f:
        expected_json_str = f.read()

    assert expected_json_str
