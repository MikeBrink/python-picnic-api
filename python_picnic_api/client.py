from .session import PicnicAPISession
from .helper import _tree_generator, _url_generator

DEFAULT_URL = "https://storefront-prod.{}.picnicinternational.com/api/{}"
DEFAULT_COUNTRY_CODE = "NL"
DEFAULT_API_VERSION = "15"


class PicnicAPI:
    def __init__(
        self, username: str, password: str, country_code: str = DEFAULT_COUNTRY_CODE
    ):
        self._username = username
        self._password = password
        self._country_code = country_code
        self._base_url = _url_generator(
            DEFAULT_URL, self._country_code, DEFAULT_API_VERSION
        )

        self.session = PicnicAPISession()
        self.session.login(self._username, self._password, self._base_url)

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
