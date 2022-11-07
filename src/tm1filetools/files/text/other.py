import configparser
from pathlib import Path

from .text import TM1TextFile


class TM1LoginCfgFile(TM1TextFile):
    """
    A class representation of a config.in file often used in TM1py examples

    """

    def __init__(self, path: Path, section: str):

        # list of valid params

        self._valid_params = [
            "address",
            "port",
            "user",
            "password",
            "ssl",
        ]

        super().__init__(path)

        self.config = configparser.ConfigParser()
        self.config.read(path, encoding=self.encoding)

        self._section = section

        self._params = {}
        self._set_params()

    def get_parameter(self, param: str) -> str:

        return self.config.get(section=self._section, option=param, fallback=None)

    def set_parameter(self, param: str, value: str) -> None:

        # if we have a list of valid options, we could warn when an invalid option set
        # do I need to care about the section in this file?
        self.config[self._section][param] = value

        with open(self._path, "w") as f:
            self.config.write(f)

    def is_valid(self):
        # check file has the necessary sections and mandatory params

        return (
            self.config.has_section(self._section)
            and self._params.get("address") is not None  # noqa
            and self._params.get("port") is not None  # noqa
            and self._params.get("user") is not None  # noqa
            and self._params.get("password") is not None  # noqa
        )

    def _set_params(self):

        for p in self._valid_params:
            self._params[p] = self.get_parameter(param=p)

    def get_login_kwargs(self):
        """
        Return a dict object suitable for as keyword arguments to create a TM1py service object
        """

        # this is very naive for now and is really only meant for local testing with
        # username/password authentication
        # note it will return all valid params found
        # it doesn't do much validation

        if self.is_valid():
            kwargs = {}
            for p, v in self._params.items():
                if v is not None:
                    kwargs[p] = v
            return kwargs
