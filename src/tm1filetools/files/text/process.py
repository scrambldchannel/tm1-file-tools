from pathlib import Path

from .text import TM1TextFile


class TM1ProcessFile(TM1TextFile):
    """
    A class representation of a tm1 TI process file. A TM1 .pro file


    """

    suffix = "pro"

    # line codes

    def __init__(self, path: Path):

        super().__init__(path)

    # Attempt some simple parsing

    # https://gist.github.com/scrambldchannel/9955cb731f80616c706f2d5a81b82c2a

    def _find_line_by_code(self, linecode):

        lines = []
        # just need to remember how to read a file line by line here
        for line in self.readlines():
            if line[0:3] == linecode:
                lines.append(line)

        return lines
