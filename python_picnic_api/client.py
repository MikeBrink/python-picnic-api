from .session import PicnicAPISession
from .config_handler import ConfigHandler
from .helper import _tree_generator


class PicnicAPI:
    def __init__(
        self,
        username: str = None,
        password: str = None,
        country_code: str = None,
        store: bool = False,
    ):
        config = ConfigHandler(
            username=username, password=password, country_code=country_code, store=store
        )
        self._base_url = self._url(config)
        self._username = config["username"]
        self._password = config["password"]

        if username and password:
            self._username = username
            self._password = password
            if store:
                config.set_username(username)
                config.set_password(password)
                config.set_country_code(country_code)

        elif "username" in config.keys() and "password" in config.keys():
            self._username = config["username"]
            self._password = config["password"]

        else:
            raise Exception("No username and/or password set")

        self.session = PicnicAPISession()
        self.session.login(self._username, self._password, self._base_url)

    def _url(self, config):
        return (
            config["base_url"].format(config["country_code"].lower())
            + config["api_version"]
        )

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

    def get_lists(self, listId: str = None):
        if listId:
            path = "/lists/" + listId
        else:
            path = "/lists"
        return self._get(path)

    def get_cart(self):
        return self._get("/cart")

    def add_product(self, productId: str, count: int = 1):
        data = {"product_id": productId, "count": count}
        return self._post("/cart/add_product", data)

    def remove_product(self, productId: str, count: int = 1):
        data = {"product_id": productId, "count": count}
        return self._post("/cart/remove_product", data)

    def clear_cart(self):
        return self._post("/cart/clear")

    def get_delivery_slots(self):
        return self._get("/cart/delivery_slots")

    def get_delivery(self, deliveryId: str):
        path = "/deliveries/" + deliveryId
        return self._get(path)

    def get_deliveries(self, summary: bool = False):
        data = []
        if summary:
            return self._post("/deliveries/summary", data=data)
        return self._post("/deliveries", data=data)

    def get_current_deliveries(self):
        data = ["CURRENT"]
        return self._post("/deliveries", data=data)

    def get_categories(self, depth: int = 0):
        return self._get(f"/my_store?depth={depth}")["catalog"]

    def print_categories(self, depth: int = 0):
        tree = "\n".join(_tree_generator(self.get_categories(depth=depth)))
        print(tree)


__all__ = ["PicnicAPI"]
