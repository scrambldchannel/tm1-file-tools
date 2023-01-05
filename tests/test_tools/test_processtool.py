from tm1filetools.tools.processtool import TM1ProcessFileTool


def test_files_generator(data_folder):

    pt = TM1ProcessFileTool(path=data_folder)

    all_procs = [p for p in pt._files()]

    assert all_procs
    assert len(all_procs)


def test_get_all_procs(data_folder):

    pt = TM1ProcessFileTool(data_folder)

    procs = pt.get_all()

    assert len(procs) == 7


def test_get_model_procs(data_folder):

    pt = TM1ProcessFileTool(data_folder)

    procs = pt.get_all_model()

    assert len(procs) == 6


def test_get_control_procs(data_folder):

    pt = TM1ProcessFileTool(data_folder)

    procs = pt.get_all_control()

    assert any(p.stem == "}control_process" for p in procs)
