from tm1filetools.files import TM1AttributeDimensionFile
from tm1filetools.tools import TM1FileTool


def test_get_attr_dims(test_folder):

    ft = TM1FileTool(test_folder)

    dims = ft.get_attr_dims()

    assert any(d.stem == f"{TM1AttributeDimensionFile.prefix}kangaroo" for d in dims)
    assert all(d.stem != f"{TM1AttributeDimensionFile.prefix}vampire" for d in dims)
    assert all(d.stem != "kangaroo" for d in dims)
