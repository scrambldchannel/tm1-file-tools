from tm1filetools.files.base import TM1File


def test_init():

    # lazy and not os safe
    path_name = "test/chimpy.rux"

    f = TM1File(path_name)

    assert f
