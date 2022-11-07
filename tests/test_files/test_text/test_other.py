from pathlib import Path

from tm1filetools.files.text.other import TM1LoginCfgFile


def test_read_and_write(test_folder):

    f = TM1LoginCfgFile(Path.joinpath(test_folder, "auth.cfg"), section="local")

    # need to create the section
    f.config.add_section(f._section)

    param = "address"

    assert f.get_parameter(param) is None

    value = "192.168.0.111"

    f.set_parameter(param, value)

    assert f.get_parameter(param) == value

    # also re-open file to check it's been written to disk

    f2 = TM1LoginCfgFile(Path.joinpath(test_folder, "auth.cfg"), section="local")

    assert f2.get_parameter(param) == value


def test_is_valid(login_config_folder):

    f = TM1LoginCfgFile(Path.joinpath(login_config_folder, "good_login.ini"), section="local")

    assert f.is_valid()

    f = TM1LoginCfgFile(Path.joinpath(login_config_folder, "vad_login.ini"), section="local")

    assert not f.is_valid()


def test_get_kwargs(login_config_folder):

    f = TM1LoginCfgFile(Path.joinpath(login_config_folder, "good_login.ini"), section="local")

    login_kwargs = f.get_login_kwargs()

    assert login_kwargs["address"] == "192.168.0.111"
    assert login_kwargs["port"] == "18081"
    assert login_kwargs["user"] == "admin"
    assert login_kwargs["password"] == "apple"

    assert login_kwargs.get("ssl") is None
    assert login_kwargs.get("irrelevant") is None

    f = TM1LoginCfgFile(Path.joinpath(login_config_folder, "messy_login.ini"), section="messy")

    login_kwargs = f.get_login_kwargs()

    assert login_kwargs["address"] == "192.168.0.111"
    assert login_kwargs["port"] == "18081"
    assert login_kwargs["user"] == "admin"
    assert login_kwargs["password"] == "apple"

    assert login_kwargs.get("ssl") is None
    assert login_kwargs.get("irrelevant") is None

    f = TM1LoginCfgFile(Path.joinpath(login_config_folder, "bad_login.ini"), section="local")

    assert f.get_login_kwargs() is None
