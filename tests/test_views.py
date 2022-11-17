
from website import create_app
import json

import pytest


def create_account(client):
    client.post("/signup", 
                data={"email": "gru@minions.org",
                        "password1": "12345678",
                        "password2": "12345678"})

    client.post("/login", 
                data={"email": "gru@minions.org",
                        "password": "12345678"})


def test_home(client):

    response = client.get('/')
    print(response.data)
    assert response.status_code == 302 # redirect to login page
    assert b'Redirecting' in response.data
    assert b'login' in response.data


    create_account(client)

    response = client.get('/', follow_redirects=True)
    print(response.data)
    assert response.status_code == 200 # redirect to login page
    assert b'Write your todo items here:' in response.data


def test_add_note(client):
    
    create_account(client)

    response = client.post("/", 
                            data={"item": "test note"})
    assert response.status_code == 200 # STAY ON home page
    assert b'Write your todo items here:' in response.data

    response = client.get('/', follow_redirects=True)
    print(response.data)
    assert response.status_code == 200 # redirect to login page
    assert b'test note' in response.data


def test_remove(client):

    test_add_note(client)

    client.get('/remove/1', follow_redirects=True)

    response = client.get('/', follow_redirects=True)
    print(response.data)
    assert response.status_code == 200 # redirect to login page
    assert b'test note' not in response.data