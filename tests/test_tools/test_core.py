from tm1filetools.tools import TM1FileTool


def test_case_insensitive_glob(test_folder):

    # pretty trivial tests but do seem to work
    # i.e. an empty list is false
    assert list(TM1FileTool._case_insensitive_glob(path=test_folder, pattern="tm1s.cfg"))
    assert not list(TM1FileTool._case_insensitive_glob(path=test_folder, pattern="THIS_FILE_DOES_NOT_EXIST"))
    assert list(TM1FileTool._case_insensitive_glob(path=test_folder, pattern="tm1s.CFG"))
    assert list(TM1FileTool._case_insensitive_glob(path=test_folder, pattern="TM1s.cFg"))


def test_find_files_by_suffix(test_folder):

    ft = TM1FileTool(test_folder)

    dims = list(ft._find_files(suffix="dim"))

    assert dims

    exes = list(ft._find_files(suffix="exes"))

    assert not exes


def test_find_dims(test_folder):

    ft = TM1FileTool(test_folder)

    assert any(d.stem == "koala" for d in ft._dim_files)
    assert all(d.stem != "bunyip" for d in ft._dim_files)

    dims = ft._find_dims()

    assert any(d.stem == "koala" for d in dims)
    assert all(d.stem != "bunyip" for d in dims)


def test_find_cubes(test_folder):
    ft = TM1FileTool(test_folder)

    assert any(c.stem == "cat" for c in ft._cube_files)
    assert all(c.stem != "unicorn" for c in ft._cube_files)

    cubes = ft._find_cubes()

    assert any(c.stem == "cat" for c in cubes)
    assert all(c.stem != "unicorn" for c in cubes)


def test_find_rules(test_folder):

    ft = TM1FileTool(test_folder)

    assert any(r.stem == "dog" for r in ft._rules_files)
    assert all(r.stem != "basilisk" for r in ft._rules_files)

    rules = ft._find_rules()

    assert any(r.stem == "dog" for r in rules)
    assert all(r.stem != "basilisk" for r in rules)


def test_find_subs(test_folder):

    ft = TM1FileTool(test_folder)

    assert any(s.stem == "platypus" for s in ft._sub_files)
    assert all(s.stem != "womble" for s in ft._sub_files)

    subs = ft._find_subs()

    assert any(s.stem == "platypus" for s in subs)
    assert all(s.stem != "womble" for s in subs)


def test_find_views(test_folder):

    ft = TM1FileTool(test_folder)

    assert any(v.stem == "mouse" for v in ft._view_files)
    assert all(v.stem != "dragon" for v in ft._view_files)

    views = ft._find_views()

    assert any(v.stem == "mouse" for v in views)
    assert all(v.stem != "dragon" for v in views)


def test_find_feeders(test_folder):

    ft = TM1FileTool(test_folder)
    assert any(f.stem == "cat" for f in ft._feeders_files)
    assert all(f.stem != "dragon" for f in ft._feeders_files)


def test_re_scan(test_folder):

    ft = TM1FileTool(test_folder)

    assert any(f.stem == "cat" for f in ft._feeders_files)

    for f in ft._feeders_files:
        if f.stem == "cat":
            f.delete()

    assert any(f.stem == "cat" for f in ft._feeders_files)

    ft.re_scan()

    assert all(f.stem != "cat" for f in ft._feeders_files)


def test_non_tm1_files(test_folder):

    ft = TM1FileTool(test_folder)

    assert any(f.name == "cat.cub.bak" for f in ft._non_tm1_files)

    for f in ft._non_tm1_files:
        if f.name == "cat.cub.bak":
            f.delete()

    assert any(f.name == "cat.cub.bak" for f in ft._non_tm1_files)

    ft.re_scan()

    assert all(f.name != "cat.cub.bak" for f in ft._non_tm1_files)


def test_find_logs(rel_config_folder):

    ft = TM1FileTool(rel_config_folder)

    assert any(log.stem == "tm1s" for log in ft._log_files)
    assert all(log.stem != "dog" for log in ft._log_files)

    logs = ft._find_logs()

    assert any(log.stem == "tm1server" for log in logs)
    assert all(log.stem != "cat" for log in logs)
