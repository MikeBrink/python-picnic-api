from python_picnic_api.session import PicnicAPISession
from python_picnic_api.config_handler import ConfigHandler
from requests import Session


def test_init():
    assert issubclass(PicnicAPISession, Session)


def test_login():
    config = ConfigHandler()
    username = config["username"]
    password = config["password"]

    session = PicnicAPISession()
    session.login(username, password)
    assert "x-picnic-auth" in session.headers.keys()


# TO DO: add test for wrong credentials
