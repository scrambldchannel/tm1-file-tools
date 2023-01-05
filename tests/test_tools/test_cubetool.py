from tm1filetools.files import TM1AttributeCubeFile
from tm1filetools.tools.cubetool import TM1CubeFileTool


def test_files_generator(data_folder):

    ct = TM1CubeFileTool(path=data_folder)

    all_cubes = [c for c in ct._files()]

    assert all_cubes
    assert len(all_cubes)


def test_get_all(data_folder):

    ct = TM1CubeFileTool(path=data_folder)

    all_cubes = ct.get_all()

    assert all_cubes
    assert len(all_cubes)

    assert any(c.stem == "}ElementAttributes_koala" for c in ct.get_all())

    assert any(c.stem == "cat" for c in ct.get_all())


def test_get_model_cubes(data_folder):

    ct = TM1CubeFileTool(path=data_folder)

    cubes = ct.get_all_model()

    assert any(c.stem == "cat" for c in cubes)
    assert all(c.stem != f"{TM1AttributeCubeFile.prefix}cat" for c in cubes)


def test_get_control_cubes(data_folder):

    ct = TM1CubeFileTool(path=data_folder)

    cubes = ct.get_all_control()

    assert any(c.stem == f"{TM1AttributeCubeFile.prefix}koala" for c in cubes)
    assert all(c.stem != "koala" for c in cubes)


def test_get_attr(data_folder):

    ft = TM1CubeFileTool(data_folder)

    cubes = ft.get_all_attr()

    assert any(c.stem == f"{TM1AttributeCubeFile.prefix}koala" for c in cubes)
    assert all(c.stem != f"{TM1AttributeCubeFile.prefix}ghoul" for c in cubes)
    assert all(c.stem != "koala" for c in cubes)
