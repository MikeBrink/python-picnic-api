from python_picnic_api import PicnicAPI


def test_get_user():
    picnic = PicnicAPI()
    response = picnic.get_user()
    assert isinstance(response, dict)


def test_search():
    picnic = PicnicAPI()
    response = picnic.search("koffie")
    assert isinstance(response, list)


def test_get_cart():
    picnic = PicnicAPI()
    response = picnic.get_cart()
    assert isinstance(response, dict)


def test_add_product():
    picnic = PicnicAPI()
    response = picnic.add_product("10407428")
    assert isinstance(response, dict)


def test_remove_product():
    picnic = PicnicAPI()
    response = picnic.remove_product("10407428")
    assert isinstance(response, dict)


def test_clear_cart():
    picnic = PicnicAPI()
    response = picnic.clear_cart()
    assert isinstance(response, dict)


def test_get_delivery_slots():
    picnic = PicnicAPI()
    response = picnic.get_delivery_slots()
    assert isinstance(response, dict)


def test_get_current_deliveries():
    picnic = PicnicAPI()
    response = picnic.get_current_deliveries()
    assert isinstance(response, list)

# TO DO: add test for re-logging
