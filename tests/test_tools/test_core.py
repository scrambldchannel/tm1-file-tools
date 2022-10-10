import sys

import pytest

from tm1filetools.files import TM1CfgFile
from tm1filetools.tools import TM1FileTool


def test_case_insensitive_glob(test_folder):

    # pretty trivial tests but do seem to work
    # i.e. an empty list is false
    assert list(TM1FileTool._case_insensitive_glob(path=test_folder, pattern="tm1s.cfg"))
    assert not list(TM1FileTool._case_insensitive_glob(path=test_folder, pattern="THIS_FILE_DOES_NOT_EXIST"))
    assert list(TM1FileTool._case_insensitive_glob(path=test_folder, pattern="tm1s.CFG"))
    assert list(TM1FileTool._case_insensitive_glob(path=test_folder, pattern="TM1s.cFg"))


def test_get_config_file(test_folder, empty_folder):

    ft = TM1FileTool(path=empty_folder)

    assert not ft.config_file

    ft = TM1FileTool(path=test_folder)

    assert ft.config_file

    assert isinstance(ft.config_file, TM1CfgFile)


def test_get_data_path_no_cfg(empty_folder):

    # if config file not found, should just be the original path
    ft = TM1FileTool(path=empty_folder)

    assert ft.data_path == empty_folder


def test_get_log_path_no_cfg(empty_folder):

    # if config file not found, should just be the original path
    ft = TM1FileTool(path=empty_folder)

    assert ft.log_path == empty_folder


def test_get_data_path_invalid_cfg(invalid_config_folder):

    ft = TM1FileTool(path=invalid_config_folder)

    assert ft.data_path == invalid_config_folder


def test_get_log_path_invalid_cfg(invalid_config_folder):

    ft = TM1FileTool(path=invalid_config_folder)

    assert ft.log_path == invalid_config_folder


def test_get_data_path_local(abs_config_folder, rel_config_folder):

    # the constructor requires a concrete path
    # which I can't find a way to instantiate cross platform
    if not sys.platform.startswith("win"):
        pytest.skip("skipping windows-only tests")

    # an absolute path is only going to get returned running locally
    ft = TM1FileTool(path=abs_config_folder, local=True)

    assert ft.data_path.is_absolute()

    ft = TM1FileTool(path=rel_config_folder, local=True)

    assert not ft.data_path.is_absolute()


def test_get_log_path_local(abs_config_folder, rel_config_folder):

    # the constructor requires a concrete path
    # which I can't find a way to instantiate cross platform
    if not sys.platform.startswith("win"):
        pytest.skip("skipping windows-only tests")

    # an absolute path is only going to get returned running locally
    ft = TM1FileTool(path=abs_config_folder, local=True)

    assert ft.log_path.is_absolute()

    ft = TM1FileTool(path=rel_config_folder, local=True)

    assert not ft.log_path.is_absolute()


def test_get_data_path_rel(rel_config_folder):

    ft = TM1FileTool(path=rel_config_folder)

    assert ft.data_path.is_absolute()
    assert ft.data_path.exists()


def test_get_log_path_rel(rel_config_folder):

    ft = TM1FileTool(path=rel_config_folder)

    assert ft.log_path.is_absolute()
    assert ft.log_path.exists()


def test_find_files_by_suffix(test_folder):

    ft = TM1FileTool(test_folder)

    dims = list(ft._find_files(suffix="dim"))

    assert dims

    exes = list(ft._find_files(suffix="exes"))

    assert not exes


def test_find_dims(test_folder):

    ft = TM1FileTool(test_folder)

    assert any(d.stem == "koala" for d in ft.dim_files)
    assert all(d.stem != "bunyip" for d in ft.dim_files)

    dims = ft._find_dims()

    assert any(d.stem == "koala" for d in dims)
    assert all(d.stem != "bunyip" for d in dims)


def test_find_cubes(test_folder):
    ft = TM1FileTool(test_folder)

    assert any(c.stem == "cat" for c in ft.cube_files)
    assert all(c.stem != "unicorn" for c in ft.cube_files)

    cubes = ft._find_cubes()

    assert any(c.stem == "cat" for c in cubes)
    assert all(c.stem != "unicorn" for c in cubes)


def test_find_rules(test_folder):

    ft = TM1FileTool(test_folder)

    assert any(r.stem == "dog" for r in ft.rules_files)
    assert all(r.stem != "basilisk" for r in ft.rules_files)

    rules = ft._find_rules()

    assert any(r.stem == "dog" for r in rules)
    assert all(r.stem != "basilisk" for r in rules)


def test_find_subs(test_folder):

    ft = TM1FileTool(test_folder)

    assert any(s.stem == "platypus" for s in ft.sub_files)
    assert all(s.stem != "womble" for s in ft.sub_files)

    subs = ft._find_subs()

    assert any(s.stem == "platypus" for s in subs)
    assert all(s.stem != "womble" for s in subs)


def test_find_views(test_folder):

    ft = TM1FileTool(test_folder)

    assert any(v.stem == "mouse" for v in ft.view_files)
    assert all(v.stem != "dragon" for v in ft.view_files)

    views = ft._find_views()

    assert any(v.stem == "mouse" for v in views)
    assert all(v.stem != "dragon" for v in views)


def test_find_feeders(test_folder):

    ft = TM1FileTool(test_folder)
    print(ft.feeders_files)
    assert any(f.stem == "cat" for f in ft.feeders_files)
    assert all(f.stem != "dragon" for f in ft.feeders_files)

    feeders = ft._find_feeders()

    assert any(f.stem == "cat" for f in feeders)
    assert all(f.stem != "dragon" for f in feeders)


def test_re_scan(test_folder):

    ft = TM1FileTool(test_folder)

    assert any(f.stem == "cat" for f in ft.feeders_files)

    for f in ft.feeders_files:
        if f.stem == "cat":
            f.delete()

    assert any(f.stem == "cat" for f in ft.feeders_files)

    ft.re_scan()

    assert all(f.stem != "cat" for f in ft.feeders_files)


def test_non_tm1_files(test_folder):

    ft = TM1FileTool(test_folder)

    assert any(f.name == "cat.cub.bak" for f in ft.non_tm1_files)

    for f in ft.non_tm1_files:
        if f.name == "cat.cub.bak":
            f.delete()

    assert any(f.name == "cat.cub.bak" for f in ft.non_tm1_files)

    ft.re_scan()

    assert all(f.name != "cat.cub.bak" for f in ft.non_tm1_files)


def test_find_logs(rel_config_folder):

    ft = TM1FileTool(rel_config_folder)

    assert any(log.stem == "tm1s" for log in ft.log_files)
    assert all(log.stem != "dog" for log in ft.log_files)

    logs = ft._find_logs()

    assert any(log.stem == "tm1server" for log in logs)
    assert all(log.stem != "cat" for log in logs)
