from python_picnic_api import PicnicAPI
from dotenv import load_dotenv
import os

load_dotenv()

username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
country_code = os.getenv("COUNTRY_CODE")

picnic = PicnicAPI(username, password, country_code=country_code)


def _get_amount(cart: dict, product_id: str):
    items = cart["items"][0]["items"]
    product = next((item for item in items if item["id"] == product_id), None)
    return product["decorators"][0]["quantity"]


def test_get_user():
    response = picnic.get_user()
    assert isinstance(response, dict)
    assert "contact_email" in response.keys()
    assert response["contact_email"] == username


def test_search():
    response = picnic.search("koffie")
    assert isinstance(response, list)
    assert isinstance(response[0], dict)
    assert "id" in response[0].keys()
    assert response[0]["id"] == "koffie"


def test_get_article():
    response = picnic.get_article("s1001546")
    assert isinstance(response, dict)
    assert "id" in response.keys()
    assert response["id"] == "s1001546"
    assert response["name"] == "Douwe Egberts aroma rood filterkoffie"
    

def test_get_lists():
    response_1 = picnic.get_lists()
    response_2 = picnic.get_lists("21725")
    assert isinstance(response_1, list)
    assert isinstance(response_2, list)


def test_get_cart():
    response = picnic.get_cart()
    assert isinstance(response, dict)
    assert "id" in response.keys()
    assert response["id"] == "shopping_cart"


def test_add_product():
    # need a clear cart for reproducibility
    picnic.clear_cart()
    response = picnic.add_product("10407428", count=2)

    assert isinstance(response, dict)
    assert "items" in response.keys()
    assert any(item["id"] == "10407428" for item in response["items"][0]["items"])
    assert _get_amount(response, "10407428") == 2


def test_remove_product():
    # need a clear cart for reproducibility
    picnic.clear_cart()
    # add two coffee to the cart so we can remove 1
    picnic.add_product("10407428", count=2)

    response = picnic.remove_product("10407428", count=1)
    amount = _get_amount(response, "10407428")

    assert isinstance(response, dict)
    assert "items" in response.keys()
    assert amount == 1


def test_clear_cart():
    # need a clear cart for reproducibility
    picnic.clear_cart()
    # add two coffee to the cart so we can clear it
    picnic.add_product("10407428", count=2)

    response = picnic.clear_cart()

    assert isinstance(response, dict)
    assert "items" in response.keys()
    assert len(response["items"]) == 0


def test_get_delivery_slots():
    response = picnic.get_delivery_slots()
    assert isinstance(response, dict)
    assert "delivery_slots" in response.keys()
    assert isinstance(response["delivery_slots"], list)


def test_get_deliveries():
    response_1 = picnic.get_deliveries()
    response_2 = picnic.get_deliveries(summary=True)

    assert isinstance(response_1, list)
    assert isinstance(response_1[0], dict)
    assert response_1[0]["type"] == "DELIVERY"

    assert isinstance(response_2, list)
    assert isinstance(response_2[0], dict)

    assert response_1 != response_2


def test_get_delivery():
    # get a id to test against
    response = picnic.get_deliveries()
    deliveryId = response[0]["id"]

    response = picnic.get_delivery(deliveryId)
    assert isinstance(response, dict)
    assert response["type"] == "DELIVERY"
    assert response["id"] == deliveryId


def test_get_current_deliveries():
    response = picnic.get_current_deliveries()
    assert isinstance(response, list)


def test_get_categories():
    response = picnic.get_categories()
    assert isinstance(response, list)


def test_print_categories(capsys):
    picnic.print_categories()
    captured = capsys.readouterr()

    assert isinstance(captured.out, str)


# TO DO: add test for re-logging
