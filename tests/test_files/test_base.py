from tm1filetools.files.base import TM1File


def test_init(tm1_file_tool_test):

    f = TM1File("cat.cub")

    assert f
