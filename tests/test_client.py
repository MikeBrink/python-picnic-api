from python_picnic_api import PicnicAPI

import os
import pytest


def test_no_user_credentials():
    if os.path.isfile("./python_picnic_api/config/app.yaml"):
        # TO DO: rename file, assert exception, return file
        pass

    connection = PicnicAPI()


def test_wrong_user_credentials():
    with pytest.raises(Exception) as context:
        c = PicnicAPI("test@test.com", "test")

    assert str(context.value) == "wrong user credentials"
