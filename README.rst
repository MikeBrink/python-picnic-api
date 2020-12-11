"""""""""""""""""
Python-Picnic-API
"""""""""""""""""

.. image:: https://camo.githubusercontent.com/cd005dca0ef55d7725912ec03a936d3a7c8de5b5/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f6275792532306d6525323061253230636f666665652d646f6e6174652d79656c6c6f772e737667
    :target: https://www.buymeacoffee.com/MikeBrink
    :alt: Buy me a coffee

Unofficial Python wrapper for the Picnic_ API. While not all API methods have been implemented yet, you'll find most of what you need to build a working application are available. 

This library is not affiliated with Picnic and retrieves data from the endpoints of the mobile application. Use at your own risk.

.. _Picnic: https://picnic.app/nl/

===============
Getting started
===============
The easiest way to install is directly from pip::

    $ pip install python-picnic-api


-----
Usage
-----
I'll go over a few common operations here you'll most likely use in applications. 
To login:

.. code-block:: python

    from python_picnic_api import PicnicAPI

    picnic = PicnicAPI(username='username', password='password', country_code="NL")

The country_code parameter defaults to NL, but you have to change it if you live in a different country than the Netherlands (Germany: DE, Belgium: BE).
You can also store your credentials by setting the store value to true, this will store your credentials and country_code in /config/app.yaml. 

Searching for a product
-----------------------
.. code-block:: python

    >>> picnic.search('coffee')
    [{'type': 'CATEGORY', 'id': 'coffee', 'links': [{'type': 'SEARCH', 'href': 'https://storefront-prod.nl.picnicinternational.com/api/15/search?search_term=coffee'}], 'name': 'coffee', 'items': [{'type': 'SINGLE_ARTICLE', 'id': '10511523', 'decorators': [{'type': 'UNIT_QUANTITY', 'unit_quantity_text': '500 gram'}], 'name': 'Lavazza espresso koffiebonen', 'display_price': 599, 'price': 599, 'image_id': 'd3fb2888fc41514bc06dfd6b52f8622cc222d017d2651501f227a537915fcc4f', 'max_count': 50, 'unit_quantity': '500 gram', 'unit_quantity_sub': '€11.98/kg', 'tags': []}, ... 

Check cart
----------
.. code-block:: python

    >>> picnic.get_cart()
    {'type': 'ORDER', 'id': 'shopping_cart', 'items': [], 'delivery_slots': [...


Manipulating your cart
----------------------
All of these methods will return the shopping cart.

.. code-block:: python

    # adding 2 'Lavazza espresso koffiebonen' to cart
    picnic.add_product('10511523', count=2)

    # removing 1 'Lavazza espresso koffiebonen' from cart
    picnic.remove_product('10511523')

    # clearing the cart
    picnic.clear_cart()

See upcoming deliveries
------------------------
.. code-block:: python

    >>> picnic.get_current_deliveries()
    []


See available delivery slots
----------------------------
.. code-block:: python

    >>> picnic.get_delivery_slots()

