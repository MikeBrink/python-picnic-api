import unittest
from unittest.mock import patch

from requests import Session

from python_picnic_api.session import PicnicAPISession


class TestSession(unittest.TestCase):
    class MockResponse:
        def __init__(self, headers):
            self.headers = headers

    @patch.object(Session, "post")
    def test_update_auth_token(self, post_mock):
        """Test that the initial auth-token is saved."""
        post_mock.return_value = self.MockResponse({
            "x-picnic-auth": "3p9fqahw3uehfaw9fh8aw3ufaw389fpawhuo3fa"
        })

        picnic_session = PicnicAPISession()
        picnic_session.post("https://picnic.app/user/login", json={"test": "data"})
        self.assertDictEqual(dict(picnic_session.headers), {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "User-Agent": "okhttp/3.9.0",
            "Content-Type": "application/json; charset=UTF-8",
            "x-picnic-auth": "3p9fqahw3uehfaw9fh8aw3ufaw389fpawhuo3fa"
        })

    @patch.object(Session, "post")
    def test_update_auth_token_refresh(self, post_mock):
        """Test that the auth-token is updated if a new one is given in the response headers."""
        post_mock.return_value = self.MockResponse({
            "x-picnic-auth": "renewed-auth-token"
        })

        picnic_session = PicnicAPISession(auth_token="initial-auth-token")
        self.assertEqual(picnic_session.auth_token, "initial-auth-token")

        picnic_session.post("https://picnic.app", json={"test": "data"})
        self.assertEqual(picnic_session.auth_token, "renewed-auth-token")

        self.assertDictEqual(dict(picnic_session.headers), {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "User-Agent": "okhttp/3.9.0",
            "Content-Type": "application/json; charset=UTF-8",
            "x-picnic-auth": "renewed-auth-token"
        })

    def test_authenticated_with_auth_token(self):
        picnic_session = PicnicAPISession(auth_token=None)
        self.assertFalse(picnic_session.authenticated)
        self.assertIsNone(picnic_session.headers[picnic_session.AUTH_HEADER])

        picnic_session = PicnicAPISession(auth_token="3p9aw8fhzsefaw29f38h7p3fwuefah37f8kwg3i")
        self.assertTrue(picnic_session.authenticated)
        self.assertEqual(picnic_session.headers[picnic_session.AUTH_HEADER], "3p9aw8fhzsefaw29f38h7p3fwuefah37f8kwg3i")
