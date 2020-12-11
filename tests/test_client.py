from python_picnic_api import PicnicAPI
from dotenv import load_dotenv
import os

load_dotenv()

username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
country_code = os.getenv("COUNTRY_CODE")

picnic = PicnicAPI(username, password, country_code=country_code)


def test_get_user():
    response = picnic.get_user()
    assert isinstance(response, dict)


def test_search():
    response = picnic.search("koffie")
    assert isinstance(response, list)


def test_get_lists():
    response_1 = picnic.get_lists()
    response_2 = picnic.get_lists("21725")
    assert isinstance(response_1, list)
    assert isinstance(response_2, list)


def test_get_cart():
    response = picnic.get_cart()
    assert isinstance(response, dict)


def test_add_product():
    response = picnic.add_product("10407428")
    assert isinstance(response, dict)


def test_remove_product():
    response = picnic.remove_product("10407428")
    assert isinstance(response, dict)


def test_clear_cart():
    response = picnic.clear_cart()
    assert isinstance(response, dict)


def test_get_delivery_slots():
    response = picnic.get_delivery_slots()
    assert isinstance(response, dict)


def test_get_deliveries():
    response_1 = picnic.get_deliveries()
    response_2 = picnic.get_deliveries(summary=True)
    assert isinstance(response_1, list)
    assert isinstance(response_2, list)


def test_get_delivery():
    response = picnic.get_deliveries()
    deliveryId = response[0]["id"]
    response = picnic.get_delivery(deliveryId)
    assert isinstance(response, dict)


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
