import os
import yaml

PATH = "./python_picnic_api/config"


class ConfigHandler(dict):
    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)

        if os.path.isfile(PATH + "/default.yaml"):
            with open(PATH + "/default.yaml", "r") as stream:
                self.update(yaml.safe_load(stream))
        else:
            self.update(self._generate_default_config())

        if os.path.isfile(PATH + "/app.yaml"):
            with open(PATH + "/app.yaml", "r") as stream:
                self.update(yaml.safe_load(stream))
        else:
            self.update(self._generate_app_config())

        if self["username"] == "YOUR_USERNAME_HERE":
            del self["username"]

        if self["password"] == "YOUR_PASSWORD_HERE":
            del self["password"]

    def set_username(self, username):
        self["username"] = username
        with open(PATH + "/app.yaml", "r") as stream:
            config = yaml.safe_load(stream)

        config["username"] = username
        with open(PATH + "/app.yaml", "w") as stream:
            yaml.dump(config, stream)

    def set_password(self, password):
        self["password"] = password
        with open(PATH + "/app.yaml", "r") as stream:
            config = yaml.safe_load(stream)

        config["password"] = password
        with open(PATH + "/app.yaml", "w") as stream:
            yaml.dump(config, stream)

    def _generate_default_config(self):
        config = dict(
            base_url="https://storefront-prod.nl.picnicinternational.com/api/",
            api_version="15",
        )

        with open(PATH + "/default.yaml", "w") as stream:
            yaml.dump(config, stream)

        return config

    def _generate_app_config(self):
        config = dict(username="YOUR_USERNAME_HERE", password="YOUR_PASSWORD_HERE")

        with open(PATH + "/app.yaml", "w") as stream:
            yaml.dump(config, stream)

        return config


__all__ = ["ConfigHandler"]
