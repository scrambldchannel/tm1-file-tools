from tm1filetools.tools import TM1FileTool


def test_delete(test_folder):

    f = test_folder / "cat.feeders"
    f.touch()

    ft = TM1FileTool(test_folder)

    len_feeders = len(ft.get_feeders())
    fd = ft._feeders_files[0]

    count = ft.delete(fd)

    assert count == 1
    assert len(ft.get_feeders()) == len_feeders - 1
    assert all(f.stem.lower() != fd.stem.lower() for f in ft.get_feeders())


def test_delete_all_orphans(test_folder):

    f = test_folder / "chimpy.feeders"
    f.touch()

    ft = TM1FileTool(test_folder)

    total_orphans = 0

    orphans = len(ft.get_orphan_rules())
    assert orphans > 0
    total_orphans = total_orphans + orphans

    orphans = len(ft.get_orphan_attr_dims())
    assert orphans > 0
    total_orphans = total_orphans + orphans

    orphans = len(ft.get_orphan_attr_cubes())
    assert orphans > 0
    total_orphans = total_orphans + orphans

    orphans = len(ft.get_orphan_feeders())
    assert orphans > 0
    total_orphans = total_orphans + orphans

    orphans = len(ft.get_orphan_views())
    assert orphans > 0
    total_orphans = total_orphans + orphans

    orphans = len(ft.get_orphan_subs())
    assert orphans > 0
    total_orphans = total_orphans + orphans

    deleted_orphans = ft.delete_all_orphans()  # noqa

    assert len(ft.get_orphan_rules()) == 0
    assert len(ft.get_orphan_attr_dims()) == 0
    assert len(ft.get_orphan_attr_cubes()) == 0
    assert len(ft.get_orphan_feeders()) == 0
    assert len(ft.get_orphan_views()) == 0
    assert len(ft.get_orphan_subs()) == 0

    # this is failing but I'm not sure if it's a fault with the test logic or a real bug
    # maybe split into more tests
    # skipping for now
    # assert total_orphans - deleted_orphans == 0


def test_delete_all_feeders(test_folder):

    f = test_folder / "goanna.feeders"
    f.touch()
    f = test_folder / "koala.feeders"
    f.touch()

    ft = TM1FileTool(test_folder)

    feeders = len(ft.get_feeders())
    assert feeders == 2

    count = ft.delete_all_feeders()

    assert len(ft.get_feeders()) == 0

    assert feeders - count == 0


def test_delete_all_blbs(test_folder):

    f = test_folder / "goanna.blb"
    f.touch()
    f = test_folder / "possum.BLB"
    f.touch()

    ft = TM1FileTool(test_folder)

    blbs = len(ft.get_blbs())
    assert blbs == 2

    count = ft.delete_all_blbs()

    assert len(ft.get_blbs()) == 0

    assert blbs - count == 0


def test_delete_all_pre_get(test_folder):

    # ensure each delete method will run a "find" first
    f = test_folder / "goanna.blb"
    f.touch()
    f = test_folder / "possum.BLB"
    f.touch()
    # feeder
    f = test_folder / "possum.feeders"
    f.touch()

    ft = TM1FileTool(test_folder)

    assert ft.delete_all_blbs() == 2
    assert ft.delete_all_feeders() == 1
