from hashlib import md5
from requests import Session


class PicnicAPISession(Session):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.headers.update(
            {
                "User-Agent": "okhttp/3.9.0",
                "Content-Type": "application/json; charset=UTF-8",
            }
        )

    def login(self, username: str, password: str):
        """Login function for the Picnic API.

        Args:
            username (str): username, usualy your email.
            password (str): password.
        """

        if "x-picnic-auth" in self.headers:
            self.headers.pop("x-picnic-auth", None)

        url = "https://storefront-prod.nl.picnicinternational.com/api/15/user/login"

        secret = md5(password.encode("utf-8")).hexdigest()
        data = {"key": username, "secret": secret, "client_id": 1}

        response = self.post(url, json=data)
        self.headers.update({"x-picnic-auth": response.headers["x-picnic-auth"]})


__all__ = ["PicnicAPISession"]
