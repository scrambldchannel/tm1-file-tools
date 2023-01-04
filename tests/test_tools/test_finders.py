from tm1filetools.tools import TM1FileTool


def test_find_dims(test_folder):

    ft = TM1FileTool(test_folder)

    ft._find_dims()

    assert any(d.stem == "koala" for d in ft._dim_files)
    assert all(d.stem != "bunyip" for d in ft._dim_files)


def test_find_cubes(test_folder):

    ft = TM1FileTool(test_folder)

    ft._find_cubes()

    assert any(c.stem == "cat" for c in ft._cube_files)
    assert all(c.stem != "unicorn" for c in ft._cube_files)


def test_find_rules(test_folder):

    ft = TM1FileTool(test_folder)

    ft._find_rules()

    assert any(r.stem == "dog" for r in ft._rules_files)
    assert all(r.stem != "basilisk" for r in ft._rules_files)


def test_find_procs(test_folder):

    f = test_folder / "dingo.pro"
    f.touch()
    f = test_folder / "wombat.pro"
    f.touch()

    ft = TM1FileTool(test_folder)

    assert not ft._proc_files

    ft._find_procs()

    assert len(ft._proc_files) == 2

    assert any(s.stem == "dingo" for s in ft._proc_files)
    assert all(s.stem != "womble" for s in ft._proc_files)


def test_find_subs(test_folder):

    ft = TM1FileTool(test_folder)

    ft._find_subs()

    assert any(s.stem == "platypus" for s in ft._sub_files)
    assert all(s.stem != "womble" for s in ft._sub_files)


def test_find_views(test_folder):

    ft = TM1FileTool(test_folder)

    ft._find_views()

    assert any(v.stem == "mouse" for v in ft._view_files)
    assert all(v.stem != "dragon" for v in ft._view_files)


def test_find_feeders(test_folder):

    f = test_folder / "cat.feeders"
    f.touch()
    f = test_folder / "dragon_fruit.blb"
    f.touch()

    ft = TM1FileTool(test_folder)

    ft._find_feeders()

    assert any(f.stem == "cat" for f in ft._feeders_files)
    assert all(f.stem != "dragon" for f in ft._feeders_files)


def test_find_chores(test_folder):

    f = test_folder / "quokka.Cho"
    f.touch()

    ft = TM1FileTool(test_folder)

    ft._find_chores()

    assert any(f.stem == "quokka" for f in ft._chore_files)
    assert all(f.stem != "brown_snake" for f in ft._chore_files)


def test_find_blbs(test_folder):

    f = test_folder / "kangaroo.blb"
    f.touch()
    f = test_folder / "emu.blb"
    f.touch()

    ft = TM1FileTool(test_folder)

    ft._find_blbs()

    assert any(blb.stem == "emu" for blb in ft._blb_files)
    assert all(blb.stem != "bunyip" for blb in ft._blb_files)


def test_find_non_tm1(test_folder):

    f = test_folder / "cat.cub.bak"
    f.touch()
    f = test_folder / "cat.cub"
    f.touch()

    ft = TM1FileTool(test_folder)

    ft._find_non_tm1()

    assert any(f.name == "cat.cub.bak" for f in ft._non_tm1_files)

    assert all(f.name != "cat.cub" for f in ft._non_tm1_files)
