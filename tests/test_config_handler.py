from python_picnic_api.config_handler import ConfigHandler

import os
import yaml


def test_default_config_generation():
    path = "./python_picnic_api/config/default.yaml"
    if os.path.isfile(path):
        os.remove(path)

    _ = ConfigHandler()

    assert os.path.isfile(path)


def test_app_config_generation():
    path = "./python_picnic_api/config/app.yaml"
    if os.path.isfile(path):
        os.rename(path, path[:-1])

    _ = ConfigHandler()

    assertion = os.path.isfile(path)

    os.remove(path)
    os.rename(path[:-1], path)

    assert assertion


def test_properties():
    config = ConfigHandler()
    keys = ["api", "base_url"]
    for key in keys:
        assert key in config.keys()


def test_set_username():
    config = ConfigHandler()

    if "username" in config.keys():
        original_username = config["username"]
        del config["username"]

    config.set_username("test")

    assertion1 = config["username"] == "test"

    with open("./python_picnic_api/config/app.yaml", "r") as stream:
        assertion2 = yaml.safe_load(stream)["username"] == "test"

    config.set_username(original_username)

    assert assertion1 and assertion2


def test_set_password():
    config = ConfigHandler()

    if "password" in config.keys():
        original_password = config["password"]
        del config["password"]

    config.set_password("test")

    assertion1 = config["password"] == "test"

    with open("./python_picnic_api/config/app.yaml", "r") as stream:
        assertion2 = yaml.safe_load(stream)["password"] == "test"

    config.set_password(original_password)

    assert assertion1 and assertion2
