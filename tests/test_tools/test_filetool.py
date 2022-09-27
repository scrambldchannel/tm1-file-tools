from tm1filetools.tools.filetool import TM1FileTool


def test_init(artifact_files):

    tm1_dir = TM1FileTool(path=artifact_files)

    assert tm1_dir

    assert tm1_dir._path


def test_get_name_part():

    # this is lazy and isn't portable
    name = "/random_folder/chimpy.rux"

    assert TM1FileTool._get_name_part(name) == "chimpy"


def test_case_insensitive_glob():

    pass
    # this is lazy and isn't portable
    # names = ["/random_folder/chimpy.RuX", "Trevor.blb", "julie.PRO"]

    # struggling to know how to test this :shrug:

    # assert TM1FileTool.case_insensitive_glob("RuX")
