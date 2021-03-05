from python_picnic_api.session import PicnicAPISession, PicnicAuthError
from python_picnic_api.helper import _url_generator
from requests import Session
from dotenv import load_dotenv
import os

load_dotenv()

username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
country_code = os.getenv("COUNTRY_CODE")

DEFAULT_URL = "https://storefront-prod.{}.picnicinternational.com/api/{}"
DEFAULT_API_VERSION = "15"


def test_init():
    assert issubclass(PicnicAPISession, Session)


def test_login():
    base_url = _url_generator(DEFAULT_URL, country_code, DEFAULT_API_VERSION)

    session = PicnicAPISession()
    session.login(username, password, base_url)
    assert "x-picnic-auth" in session.headers.keys()


def test_login_auth_error():
    base_url = _url_generator(DEFAULT_URL, country_code, DEFAULT_API_VERSION)

    try:
        session = PicnicAPISession()
        session.login('username', 'password', base_url)
    except PicnicAuthError:
        assert True
    else:
        assert False
