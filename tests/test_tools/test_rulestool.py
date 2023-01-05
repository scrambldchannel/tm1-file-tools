from tm1filetools.tools.rulestool import TM1RulesFileTool


def test_files_generator(data_folder):

    pt = TM1RulesFileTool(path=data_folder)

    all_procs = [p for p in pt._files()]

    assert all_procs
    assert len(all_procs)


def test_get_all(data_folder):

    rt = TM1RulesFileTool(data_folder)

    rules = rt.get_all()

    assert len(rules) == 2

    assert any(r.stem == "skipcheck_feeders" for r in rules)
    assert any(r.stem == "}ClientProperties" for r in rules)


def test_get_model(data_folder):

    rt = TM1RulesFileTool(data_folder)

    rules = rt.get_all_model()

    assert any(r.stem == "skipcheck_feeders" for r in rules)
    assert all(r.stem != "}ClientProperties" for r in rules)


def test_get_control(data_folder):

    rt = TM1RulesFileTool(data_folder)

    rules = rt.get_all_control()

    assert any(r.stem == "}ClientProperties" for r in rules)
    assert all(r.stem != "skipcheck_feeders" for r in rules)
