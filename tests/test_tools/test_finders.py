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

    ft = TM1FileTool(test_folder)

    ft._find_procs()

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

    ft = TM1FileTool(test_folder)

    ft._find_feeders()

    assert any(f.stem == "cat" for f in ft._feeders_files)
    assert all(f.stem != "dragon" for f in ft._feeders_files)


def test_find_chores(test_folder):

    ft = TM1FileTool(test_folder)

    ft._find_chores()

    assert any(f.stem == "quokka" for f in ft._chore_files)
    assert all(f.stem != "brown_snake" for f in ft._chore_files)


def test_find_logs(test_folder):

    ft = TM1FileTool(test_folder)

    ft._find_logs()

    assert any(log.stem == "tm1s" for log in ft._log_files)
    assert all(log.stem != "dog" for log in ft._log_files)


def test_find_blb(test_folder):

    ft = TM1FileTool(test_folder)

    ft._find_blbs()

    assert any(blb.stem == "emu" for blb in ft._blb_files)
    assert all(blb.stem != "bunyip" for blb in ft._blb_files)


def test_find_non_tm1(test_folder):

    ft = TM1FileTool(test_folder)

    ft._find_non_tm1()

    assert any(f.name == "cat.cub.bak" for f in ft._non_tm1_files)

    assert all(f.name != "cat.cub" for f in ft._non_tm1_files)
