from tm1filetools.files import TM1AttributeDimensionFile
from tm1filetools.tools.dimtool import TM1DimensionFileTool


def test_files_generator(data_folder):

    dt = TM1DimensionFileTool(path=data_folder)

    all_dimensions = [d for d in dt._files()]

    assert all_dimensions
    assert len(all_dimensions)


def test_get_all_dimensions(data_folder):

    dt = TM1DimensionFileTool(path=data_folder)

    all_dimensions = dt.get_all_dims()

    assert all_dimensions
    assert len(all_dimensions)

    assert any(d.stem == "}ElementAttributes_koala" for d in dt.get_all_dims())

    assert any(d.stem == "koala" for d in dt.get_all_dims())


def test_get_model_dims(data_folder):

    dt = TM1DimensionFileTool(path=data_folder)

    dimensions = dt.get_model_dims()

    assert any(d.stem == "koala" for d in dimensions)
    assert all(d.stem != f"{TM1AttributeDimensionFile.prefix}koala" for d in dimensions)


def test_get_control_dims(data_folder):

    dt = TM1DimensionFileTool(path=data_folder)

    dimensions = dt.get_control_dims()

    assert any(d.stem == f"{TM1AttributeDimensionFile.prefix}koala" for d in dimensions)
    assert all(c.stem != "koala" for c in dimensions)


def test_get_attr_dims(data_folder):

    ft = TM1DimensionFileTool(data_folder)

    dimensions = ft.get_attr_dims()

    assert any(d.stem == f"{TM1AttributeDimensionFile.prefix}koala" for d in dimensions)
    assert all(d.stem != f"{TM1AttributeDimensionFile.prefix}ghoul" for d in dimensions)
    assert all(d.stem != "koala" for d in dimensions)
