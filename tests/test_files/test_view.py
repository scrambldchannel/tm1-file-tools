from pathlib import Path

from tm1filetools.files.view import TM1ViewFile


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

    f = TM1ViewFile(Path.joinpath(test_folder, f"cat{TM1ViewFile.folder_suffix}", "squirrel.vue"))

    assert f._get_public_path() == Path.joinpath(test_folder, f"cat{TM1ViewFile.folder_suffix}")

    f = TM1ViewFile(
        Path.joinpath(test_folder, "Chimpy", f"cat{TM1ViewFile.folder_suffix}", "squirrel.vue"), public=False
    )

    new_path = f._get_public_path()

    assert new_path == Path.joinpath(test_folder, f"cat{TM1ViewFile.folder_suffix}")


def test_move_to_public(test_folder):

    f = TM1ViewFile(
        Path.joinpath(test_folder, "Chimpy", f"cat{TM1ViewFile.folder_suffix}", "squirrel.vue"), public=False
    )

    f.move_to_public()

    assert f._get_owner_name() is None
    assert f._path == Path.joinpath(test_folder, f"cat{TM1ViewFile.folder_suffix}", "squirrel.vue")

    f = TM1ViewFile(Path.joinpath(test_folder, f"cat{TM1ViewFile.folder_suffix}", "squirrel.vue"))

    assert f._get_owner_name() is None
    assert f._path == Path.joinpath(test_folder, f"cat{TM1ViewFile.folder_suffix}", "squirrel.vue")
    assert f.public
