from pathlib import Path

from tm1filetools.files import TM1ProcessFile


def test_init(test_folder):

    p = TM1ProcessFile(Path.joinpath(test_folder, "copy data from my cube.pro"))

    assert p
    assert p.suffix == "pro"


def test_find_line(test_folder):

    p = TM1ProcessFile(Path.joinpath(test_folder, "copy data from my cube.pro"))

    # build up this file and read some basic line codes

    p.write(
        r"""601,100
602,my zany process
        """
    )

    assert p._find_line_by_code(linecode="601")[0] == "601,100"

    assert p._find_line_by_code(linecode="602")[0] == "602,my zany process"
