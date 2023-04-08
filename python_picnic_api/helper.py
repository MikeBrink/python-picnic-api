import re

# prefix components:
space = "    "
branch = "│   "
# pointers:
tee = "├── "
last = "└── "


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


def _get_category_id_from_link(category_link: str) -> str:
    pattern = r'categories/(\d+)'
    first_number = re.search(pattern, category_link)
    if first_number:
        result = str(first_number.group(1))
        return result
    else:
        return None
    
    
def _get_category_name(category_link: str, categories: list) -> str:
    category_id = _get_category_id_from_link(category_link)
    if category_id:
        category = next((item for item in categories if item["id"] == category_id), None)
        if category:
            return category["name"]
        else:
            return None
    else:
        return None
