from .session import PicnicAPISession, PicnicAuthError
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

    def _get(self, path: str, add_picnic_headers=False):
        url = self._base_url + path

        # Make the request, add special picnic headers if needed
        headers = {
            "x-picnic-agent": "30100;1.15.77-10293",
            "x-picnic-did": "3C417201548B2E3B"
        } if add_picnic_headers else None
        response = self.session.get(url, headers=headers).json()

        if self._contains_auth_error(response):
            raise PicnicAuthError("Picnic authentication error")

        return response

    def _post(self, path: str, data=None):
        url = self._base_url + path
        response = self.session.post(url, json=data).json()

        if self._contains_auth_error(response):
            raise PicnicAuthError("Picnic authentication error")

        return response

    @staticmethod
    def _contains_auth_error(response):
        return isinstance(response, dict) and response.setdefault('error', {}).get('code') == 'AUTH_ERROR'

    def get_user(self):
        return self._get("/user")

    def search(self, term: str):
        path = "/search?search_term=" + term
        return self._get(path)

    def get_lists(self, list_id: str = None):
        if list_id:
            path = "/lists/" + list_id
        else:
            path = "/lists"
        return self._get(path)

    def get_cart(self):
        return self._get("/cart")

    def add_product(self, product_id: str, count: int = 1):
        data = {"product_id": product_id, "count": count}
        return self._post("/cart/add_product", data)

    def remove_product(self, product_id: str, count: int = 1):
        data = {"product_id": product_id, "count": count}
        return self._post("/cart/remove_product", data)

    def clear_cart(self):
        return self._post("/cart/clear")

    def get_delivery_slots(self):
        return self._get("/cart/delivery_slots")

    def get_delivery(self, delivery_id: str):
        path = "/deliveries/" + delivery_id
        return self._get(path)

    def get_delivery_scenario(self, delivery_id: str):
        path = "/deliveries/" + delivery_id + "/scenario"
        return self._get(path, add_picnic_headers=True)

    def get_delivery_position(self, delivery_id: str):
        path = "/deliveries/" + delivery_id + "/position"
        return self._get(path, add_picnic_headers=True)

    def get_deliveries(self, summary: bool = False, data=None):
        data = [] if data is None else data
        if summary:
            return self._post("/deliveries/summary", data=data)
        return self._post("/deliveries", data=data)

    def get_current_deliveries(self):
        return self.get_deliveries(data=["CURRENT"])

    def get_categories(self, depth: int = 0):
        return self._get(f"/my_store?depth={depth}")["catalog"]

    def print_categories(self, depth: int = 0):
        tree = "\n".join(_tree_generator(self.get_categories(depth=depth)))
        print(tree)


__all__ = ["PicnicAPI"]
