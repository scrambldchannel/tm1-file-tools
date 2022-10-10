# import pytest

from tm1filetools.tools import TM1FileTool


def test_rename(test_folder):

    ft = TM1FileTool(test_folder)

    for c in ft._cube_files:

        if c.stem == "cat":
            ft.rename(c, "lion")

    assert any(c.stem == "lion" for c in ft._cube_files)
    assert all(c.stem != "cat" for c in ft._cube_files)
