from pathlib import Path

import pytest


@pytest.fixture(scope="function")
def proc_folder():

    path = Path.joinpath(Path.cwd(), "tests", "test_files", "artifacts", "processes")

    return path


@pytest.fixture(scope="function")
def sub_folder():

    path = Path.joinpath(Path.cwd(), "tests", "test_files", "artifacts", "subsets")

    return path


@pytest.fixture(scope="function")
def view_folder():

    path = Path.joinpath(Path.cwd(), "tests", "test_files", "artifacts", "views")

    return path


@pytest.fixture(scope="function")
def cfg_folder(tmp_path_factory):

    path = Path.joinpath(Path.cwd(), "tests", "test_files", "artifacts", "cfg")

    return path

    # f.write_text(cfg)

    # f = d / "bad_login.ini"

    # cfg = r"""[local]
    # address = 192.168.0.111
    # user = admin
    # password = apple
    # """

    # f.write_text(cfg)

    # f = d / "messy_login.ini"

    # cfg = r"""[messy]
    # address = 192.168.0.111
    # port = 18081
    # user = admin
    # password = apple
    # irrelevant = koala
    # """

    # f.write_text(cfg)

    # return d
