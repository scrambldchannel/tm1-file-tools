# import pytest

from tm1filetools.files import TM1AttributeCubeFile, TM1AttributeDimensionFile
from tm1filetools.tools import TM1FileTool


def test_get_model_dims(test_folder):

    ft = TM1FileTool(test_folder)

    dims = ft.get_model_dims()

    assert any(d.stem == "koala" for d in dims)
    assert all(d.stem != f"{TM1AttributeDimensionFile.prefix}koala" for d in dims)


def test_get_control_dims(test_folder):

    ft = TM1FileTool(test_folder)

    dims = ft.get_control_dims()

    assert any(d.stem == f"{TM1AttributeDimensionFile.prefix}koala" for d in dims)
    assert all(d.stem != "koala" for d in dims)


def test_get_model_cubes(test_folder):

    ft = TM1FileTool(test_folder)

    cubes = ft.get_model_cubes()

    assert any(c.stem == "cat" for c in cubes)
    assert all(c.stem != f"{TM1AttributeCubeFile.prefix}cat" for c in cubes)


def test_get_control_cubes(test_folder):

    ft = TM1FileTool(test_folder)

    cubes = ft.get_control_cubes()

    assert any(c.stem == f"{TM1AttributeCubeFile.prefix}koala" for c in cubes)
    assert all(c.stem != "koala" for c in cubes)


def test_get_attr_cubes(test_folder):

    ft = TM1FileTool(test_folder)

    cubes = ft.get_attr_cubes()

    assert any(c.stem == f"{TM1AttributeCubeFile.prefix}koala" for c in cubes)
    assert all(c.stem != f"{TM1AttributeCubeFile.prefix}ghoul" for c in cubes)
    assert all(c.stem != "koala" for c in cubes)


def test_get_attr_dims(test_folder):

    ft = TM1FileTool(test_folder)

    dims = ft.get_attr_dims()

    assert any(d.stem == f"{TM1AttributeDimensionFile.prefix}kangaroo" for d in dims)
    assert all(d.stem != f"{TM1AttributeDimensionFile.prefix}vampire" for d in dims)
    assert all(d.stem != "kangaroo" for d in dims)


def test_get_control_processes(test_folder):

    ft = TM1FileTool(test_folder)

    procs = ft.get_control_procs()

    assert any(p.stem == "}fraggle" for p in procs)
    assert all(p.stem != "dingo" for p in procs)


def test_get_control_views(test_folder):

    ft = TM1FileTool(test_folder)

    views = ft.get_control_views()

    assert any(v.stem == "}shark" for v in views)
    assert all(v.stem != "squirrel" for v in views)
    assert all(v.stem != "donkey" for v in views)


def test_get_control_subs(test_folder):

    ft = TM1FileTool(test_folder)

    subs = ft.get_control_subs()

    assert any(s.stem == "}dolphin" for s in subs)
    assert all(s.stem != "squirrel" for s in subs)
    assert all(s.stem != "donkey" for s in subs)
