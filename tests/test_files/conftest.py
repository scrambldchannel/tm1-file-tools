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
