from tm1filetools.files import TM1AttributeCubeFile, TM1AttributeDimensionFile
from tm1filetools.tools import TM1FileTool


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
