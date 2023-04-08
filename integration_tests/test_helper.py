from python_picnic_api.helper import get_image, get_recipe_image
import requests


def test_get_image():
    id = "8560e1f1c2d2811dfefbbb2342ef0d95250533f2131416aca459bde35d73e901"
    size = "tile-medium"
    suffix = "webp"
    url = get_image(id, size=size, suffix=suffix)

    response = requests.get(url)

    # Check if the response status code indicates success
    assert response.status_code == 200, "Failed to fetch URL"

    # Check if the response content type is an image format
    content_type = response.headers.get("content-type")
    assert content_type.startswith("image/"), "URL does not return an image"


def test_get_recipe_image():
    id = "5c4cc7cb7a0429695da708394eb0cae1bd9b92935ac76c8fda63bbc57ad5b826"
    size = "medium"
    url = get_recipe_image(id, size=size)
    print(url)

    response = requests.get(url)

    # Check if the response status code indicates success
    assert response.status_code == 200, "Failed to fetch URL"

    # Check if the response content type is an image format
    content_type = response.headers.get("content-type")
    assert content_type.startswith("image/"), "URL does not return an image"
