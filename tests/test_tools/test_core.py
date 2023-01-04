from tm1filetools.tools import TM1FileTool


def test_case_insensitive_glob(test_folder):

    # pretty trivial tests but do seem to work

    assert not list(TM1FileTool._case_insensitive_glob(path=test_folder, pattern="tm1s.cfg"))

    f = test_folder / "tm1s.cfg"
    f.touch()

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


def test_find_all(test_folder):

    f = test_folder / "cat.feeders"
    f.touch()

    ft = TM1FileTool(test_folder)

    assert any(f.stem == "cat" for f in ft.get_feeders())
