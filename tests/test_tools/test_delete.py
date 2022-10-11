from tm1filetools.tools import TM1FileTool


def test_delete(test_folder):

    ft = TM1FileTool(test_folder)

    len_feeders = len(ft.get_feeders())
    fd = ft._feeders_files[0]

    ft.delete(fd)

    assert len(ft.get_feeders()) == len_feeders - 1
    assert all(f.stem.lower() != fd.stem.lower() for f in ft.get_feeders())


def test_delete_all_orphans(test_folder):

    ft = TM1FileTool(test_folder)

    assert len(ft.get_orphan_rules()) > 0
    assert len(ft.get_orphan_attr_dims()) > 0
    assert len(ft.get_orphan_attr_cubes()) > 0
    assert len(ft.get_orphan_feeders()) > 0
    assert len(ft.get_orphan_views()) > 0
    assert len(ft.get_orphan_subs()) > 0

    ft.delete_all_orphans()

    assert len(ft.get_orphan_rules()) == 0
    assert len(ft.get_orphan_attr_dims()) == 0
    assert len(ft.get_orphan_attr_cubes()) == 0
    assert len(ft.get_orphan_feeders()) == 0
    assert len(ft.get_orphan_views()) == 0
    assert len(ft.get_orphan_subs()) == 0


def test_delete_all_feeders(test_folder):

    ft = TM1FileTool(test_folder)

    assert len(ft.get_feeders()) > 0

    ft.delete_all_feeders()

    assert len(ft.get_feeders()) == 0


def test_delete_all_blbs(test_folder):

    ft = TM1FileTool(test_folder)

    assert len(ft.get_blbs()) > 0

    ft.delete_all_blbs()

    assert len(ft.get_blbs()) == 0

    ft.delete_all_blbs()

    assert len(ft.get_blbs()) == 0


def test_delete_all_pre_get(test_folder):

    # ensure each delete method will run a "find" first

    ft = TM1FileTool(test_folder)

    ft.delete_all_blbs()
    ft.delete_all_orphans()
    ft.delete_all_feeders()
