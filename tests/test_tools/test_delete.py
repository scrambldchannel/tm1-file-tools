# import pytest

from tm1filetools.tools import TM1FileTool


def test_delete(test_folder):

    ft = TM1FileTool(test_folder)

    len_feeders = len(ft.feeders_files)
    fd = ft.feeders_files[0]

    ft.delete(fd)

    assert len(ft.feeders_files) == len_feeders - 1
    assert all(f.stem.lower() != fd.stem.lower() for f in ft.feeders_files)


def test_delete_all_orphans(test_folder):

    ft = TM1FileTool(test_folder)

    assert len(ft.get_orphan_rules()) > 0
    assert len(ft.get_orphan_attr_dims()) > 0
    assert len(ft.get_orphan_attr_cubes()) > 0
    assert len(ft.get_orphan_feeders()) > 0
    assert len(ft.get_orphan_views()) > 0
    assert len(ft.get_orphan_subsets()) > 0

    ft.delete_all_orphans()

    assert len(ft.get_orphan_rules()) == 0
    assert len(ft.get_orphan_attr_dims()) == 0
    assert len(ft.get_orphan_attr_cubes()) == 0
    assert len(ft.get_orphan_feeders()) == 0
    assert len(ft.get_orphan_views()) == 0
    assert len(ft.get_orphan_subsets()) == 0


def test_delete_all_feeders(test_folder):

    ft = TM1FileTool(test_folder)

    assert len(ft.feeders_files) > 0

    ft.delete_all_feeders()

    assert len(ft.feeders_files) == 0
