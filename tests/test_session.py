import unittest
from hashlib import md5
from unittest.mock import patch

from python_picnic_api.session import PicnicAPISession, PicnicAuthError


class TestSession(unittest.TestCase):
    class MockResponse:
        def __init__(self, headers):
            self.headers = headers

    def setUp(self) -> None:
        self.picnic_session = PicnicAPISession()

    @patch.object(PicnicAPISession, 'post')
    def test_login(self, post_mock):
        post_mock.return_value = self.MockResponse({
            "x-picnic-auth": "3p9fqahw3uehfaw9fh8aw3ufaw389fpawhuo3fa"
        })

        self.picnic_session.login("test@user.nl", "test-password", "https://picnic.app")

        post_mock.assert_called_with(
            'https://picnic.app/user/login',
            json={"key": "test@user.nl", "secret": md5("test-password".encode("utf-8")).hexdigest(), "client_id": 1}
        )
        self.assertDictEqual(dict(self.picnic_session.headers), {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "User-Agent": "okhttp/3.9.0",
            "Content-Type": "application/json; charset=UTF-8",
            "x-picnic-auth": "3p9fqahw3uehfaw9fh8aw3ufaw389fpawhuo3fa"
        })

    @patch.object(PicnicAPISession, 'post')
    def test_login_failed(self, post_mock):
        post_mock.return_value = self.MockResponse({})

        with self.assertRaises(PicnicAuthError):
            self.picnic_session.login('test@user.nl', 'test-password', 'https://picnic.app')

    def test_authenticated_with_auth_token(self):
        picnic_session = PicnicAPISession(auth_token=None)
        self.assertFalse(picnic_session.authenticated())
        self.assertIsNone(picnic_session.headers[picnic_session.AUTH_HEADER])

        picnic_session = PicnicAPISession(auth_token='3p9aw8fhzsefaw29f38h7p3fwuefah37f8kwg3i')
        self.assertTrue(picnic_session.authenticated())
        self.assertEqual(picnic_session.headers[picnic_session.AUTH_HEADER], '3p9aw8fhzsefaw29f38h7p3fwuefah37f8kwg3i')
