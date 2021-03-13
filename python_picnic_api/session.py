from hashlib import md5
from requests import Session


class PicnicAuthError(Exception):
    """Indicates an error when authenticating to the Picnic API."""


class PicnicAPISession(Session):

    AUTH_HEADER = "x-picnic-auth"

    def __init__(self, auth_token=None):
        super().__init__()
        self.auth_token = auth_token

        self.headers.update(
            {
                "User-Agent": "okhttp/3.9.0",
                "Content-Type": "application/json; charset=UTF-8",
                self.AUTH_HEADER: self.auth_token
            }
        )

    def login(self, username: str, password: str, base_url: str):
        """Login function for the Picnic API.

        Args:
            username (str): username, usually your email.
            password (str): password.
            base_url (str): The base url for doing requests
        """

        if "x-picnic-auth" in self.headers:
            self.headers.pop("x-picnic-auth", None)

        url = base_url + "/user/login"

        secret = md5(password.encode("utf-8")).hexdigest()
        data = {"key": username, "secret": secret, "client_id": 1}

        response = self.post(url, json=data)
        if self.AUTH_HEADER not in response.headers:
            raise PicnicAuthError("Could not authenticate against Picnic API")

        self.auth_token = response.headers[self.AUTH_HEADER]
        self.headers.update({self.AUTH_HEADER: self.auth_token})

        return self.auth_token

    def authenticated(self):
        """Returns if the user is authenticated by checking if the authentication token is set."""
        return bool(self.auth_token)


__all__ = ["PicnicAuthError", "PicnicAPISession"]
