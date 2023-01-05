from tm1filetools.tools import TM1FileTool


def test_get_model_subs(test_folder):

    ft = TM1FileTool(test_folder)

    subs = ft.get_subs()

    assert any(s.stem == "donkey" for s in subs)
    assert all(s.stem != "}dolphin" for s in subs)


def test_get_control_subs(test_folder):

    ft = TM1FileTool(test_folder)

    subs = ft.get_subs(model=False, control=True)

    assert any(s.stem == "}dolphin" for s in subs)
    assert all(s.stem != "squirrel" for s in subs)
    assert all(s.stem != "donkey" for s in subs)


def test_get_model_views(test_folder):

    ft = TM1FileTool(test_folder)

    views = ft.get_views()

    assert any(v.stem == "squirrel" for v in views)
    assert all(v.stem != "}shark" for v in views)


def test_get_control_views(test_folder):

    ft = TM1FileTool(test_folder)

    views = ft.get_views(model=False, control=True)

    assert any(v.stem == "}shark" for v in views)
    assert all(v.stem != "squirrel" for v in views)
    assert all(v.stem != "donkey" for v in views)


def test_get_model_chores(test_folder):

    f = test_folder / "quokka.Cho"
    f.touch()
    f = test_folder / "}brown_snake.cho"
    f.touch()

    ft = TM1FileTool(test_folder)

    chores = ft.get_chores()

    assert any(c.stem == "quokka" for c in chores)
    assert all(c.stem != "brown_snake" for c in chores)
    assert all(c.stem != "}brown_snake" for c in chores)


def test_get_control_chores(test_folder):

    f = test_folder / "quokka.Cho"
    f.touch()
    f = test_folder / "}brown_snake.cho"
    f.touch()

    ft = TM1FileTool(test_folder)

    chores = ft.get_chores(model=False, control=True)

    assert any(c.stem == "}brown_snake" for c in chores)
    assert all(c.stem != "quokka" for c in chores)


def test_get_blbs(test_folder):

    f = test_folder / "emu.blb"
    f.touch()
    f = test_folder / "kangaroo.blb"
    f.touch()

    ft = TM1FileTool(test_folder)

    blbs = ft.get_blbs(control=True)

    assert len(blbs) == 2
    assert any(b.stem == "emu" for b in blbs)
    assert all(b.stem != "}shark" for b in blbs)


def test_get_cmas(test_folder):

    f = test_folder / "bunyip.cma"
    f.touch()
    f = test_folder / "magpie.CMA"
    f.touch()

    ft = TM1FileTool(test_folder)

    cmas = ft.get_cmas()

    assert any(c.stem == "bunyip" for c in cmas)
    assert any(c.stem == "magpie" for c in cmas)
    assert all(c.stem != "goanna" for c in cmas)
