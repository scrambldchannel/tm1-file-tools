from tm1filetools.tools.filetool import TM1FileTool


def test_orphan_rules(test_folder):

    ft = TM1FileTool(test_folder)

    orphans = ft.get_orphan_rules()

    assert len(orphans) > 0
    assert "foo" not in [o.stem for o in orphans]
    assert "giraffe" in [o.stem for o in orphans]
    # mixed case
    assert "}statsforserver" not in [o.stem for o in orphans]
    assert "TIGER" not in [o.stem for o in orphans]


def test_orphan_attr_dims(test_folder):

    ft = TM1FileTool(test_folder)

    orphans = ft.get_orphan_attr_dims()

    assert orphans
    assert "koala" not in [o.strip_prefix() for o in orphans]
    assert "MAGPIE" not in [o.strip_prefix() for o in orphans]
    assert "kangaroo" in [o.strip_prefix() for o in orphans]


def test_orphan_attr_cubes(test_folder):

    ft = TM1FileTool(test_folder)

    orphans = ft.get_orphan_attr_cubes()

    assert len(orphans) > 0
    assert "foo" not in [o.strip_prefix() for o in orphans]
    assert "humphrey" in [o.strip_prefix() for o in orphans]


def test_orphan_subsets(test_folder):

    ft = TM1FileTool(test_folder)

    orphans = ft.get_orphan_subs()

    assert len(orphans) > 0

    assert "koala" not in [o.dimension.lower() for o in orphans]
    assert "cat" in [o.dimension.lower() for o in orphans]


def test_orphan_views(test_folder):

    ft = TM1FileTool(test_folder)

    orphans = ft.get_orphan_views()

    assert len(orphans) > 0

    assert "cat" not in [o.cube.lower() for o in orphans]
    assert "koala" in [o.cube.lower() for o in orphans]


def test_orphan_feeders(test_folder):

    f = test_folder / "cat.feeders"
    f.touch()
    f = test_folder / "possum.feeders"
    f.touch()

    ft = TM1FileTool(test_folder)

    orphans = ft.get_orphan_feeders()

    assert len(orphans) > 0
    assert "cat" not in [o.stem for o in orphans]
    assert "possum" in [o.stem for o in orphans]
