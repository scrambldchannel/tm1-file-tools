from pathlib import Path

from tm1filetools.files import TM1FeedersFile


def test_feeders(test_folder):

    f = TM1FeedersFile(Path.joinpath(test_folder, "cat.feeders"))

    assert f
    assert f.exists
