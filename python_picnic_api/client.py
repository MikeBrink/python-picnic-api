from .session import PicnicAPISession
from .config_handler import ConfigHandler


class PicnicAPI:
    def __init__(self, username=None, password=None, store=False):
        config = ConfigHandler(username=username, password=password)
        self._base_url = config['base_url'] + config['api_version']
        self._username = config['username']
        self._password = config['password']

        if username and password:
            self._username = username
            self._password = password
            if store:
                config.set_username(username)
                config.set_password(password)

        elif "username" in config.keys() and "password" in config.keys():
            self._username = config["username"]
            self._password = config["password"]

        else:
            raise Exception("No username and/or password set")

        self.session = PicnicAPISession()
        self.session.login(self._username, self._password)

    def _get(self, path: str):
        url = self._base_url + path
        return self.session.get(url).json()

    def _post(self, path: str, data=None):
        url = self._base_url + path
        return self.session.post(url, json=data).json()

    def get_user(self):
        return self._get("/user")

    def search(self, term: str):
        path = "/search?search_term=" + term
        return self._get(path)

    def get_cart(self):
        return self._get("/cart")

    def add_product(self, productId, count=1):
        data = {"product_id": productId, "count": count}
        return self._post("/cart/add_product", data)

    def remove_product(self, productId, count=1):
        data = {"product_id": productId, "count": count}
        return self._post("/cart/remove_product", data)

    def clear_cart(self):
        return self._post("/cart/clear")

    def get_delivery_slots(self):
        return self._get("/cart/delivery_slots")

    def get_current_deliveries(self):
        data = ["CURRENT"]
        return self._post("/deliveries", data=data)


__all__ = ["PicnicAPI"]
