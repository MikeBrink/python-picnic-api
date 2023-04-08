# prefix components:
space = "    "
branch = "│   "
# pointers:
tee = "├── "
last = "└── "

IMAGE_SIZES = ["small", "medium", "regular", "large", "extra-large"]
IMAGE_BASE_URL = "https://storefront-prod.nl.picnicinternational.com/static/images"

def _tree_generator(response: list, prefix: str = ""):
    """A recursive tree generator,
    will yield a visual tree structure line by line
    with each line prefixed by the same characters
    """
    # response each get pointers that are ├── with a final └── :
    pointers = [tee] * (len(response) - 1) + [last]
    for pointer, item in zip(pointers, response):
        yield prefix + pointer + item["name"]
        if "items" in item:  # extend the prefix and recurse:
            extension = branch if pointer == tee else space
            # i.e. space because last, └── , above so no more |
            yield from _tree_generator(item["items"], prefix=prefix + extension)


def _url_generator(url: str, country_code: str, api_version: str):
    return url.format(country_code.lower(), api_version)


def get_recipe_image(id: str, size="regular"):
    sizes = IMAGE_SIZES + ["1250x1250"]
    assert size in sizes, "size must be one of: " + ", ".join(sizes)
    return f"{IMAGE_BASE_URL}/recipes/{id}/{size}.png"


def get_image(id: str, size="regular", suffix="webp"):
    assert "tile" in size if suffix == "webp" else True, (
        "webp format only supports tile sizes"
    )
    assert suffix in ["webp", "png"], "suffix must be webp or png"
    sizes = IMAGE_SIZES + [f"tile-{size}" for size in IMAGE_SIZES]

    assert size in sizes, (
        "size must be one of: " + ", ".join(sizes)
    )
    return f"{IMAGE_BASE_URL}/{id}/{size}.{suffix}"
