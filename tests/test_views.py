
from website import create_app
import json

import pytest


def test_home(client):

    response = client.get('/')
    print(response.data)
    assert response.status_code == 302 # redirect to login page
    assert b'Redirecting' in response.data
    assert b'login' in response.data