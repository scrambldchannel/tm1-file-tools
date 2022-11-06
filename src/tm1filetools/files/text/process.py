from pathlib import Path

from .text import TM1TextFile


class TM1ProcessFile(TM1TextFile):
    """
    A class representation of a tm1 TI process file. A TM1 .pro file


    """

    suffix = "pro"

    # line codes - see https://gist.github.com/scrambldchannel/9955cb731f80616c706f2d5a81b82c2a
    _linecode_lookup = {
        "601": {
            "Code": "601",
            "Descriptions": "version",
            "Java Api Name": "ProcessFileVersionNumber",
            "Multilines": False,
            "Multiline with keys": False,
        },
        "602": {
            "Code": "601",
            "Descriptions": "",
            "Java Api Name": "ProcessName",
            "Multilines": False,
            "Multiline with keys": False,
        },
    }

    def __init__(self, path: Path):

        super().__init__(path)

        self.prolog = None
        self.metadata = None
        self.data = None
        self.epilog = None

    # Attempt some simple parsing

    # https://gist.github.com/scrambldchannel/9955cb731f80616c706f2d5a81b82c2a

    def _find_line_by_code(self, linecode: int):

        lines = []
        # just need to remember how to read a file line by line here
        for line in self.readlines():

            code = line[0:3]

            if code == linecode:

                lines.append(line)

        return lines
