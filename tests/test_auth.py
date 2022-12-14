
from website import create_app
import json

import pytest


def test_failed_login(client):

    response = client.get('/login')
    assert response.status_code == 200
    assert b'email' in response.data
    assert b'password' in response.data

    with client:
        response = client.post("/login", 
                                data={"email": "gru@minions.org",
                                      "password": "12345678"})

        #print("\n\n", response.data)
        assert response.status_code == 200
        assert b'User does not exist' in response.data

def test_signup(client):

    response = client.get('/signup')
    assert response.status_code == 200
    assert b'email' in response.data
    assert b'password' in response.data

    with client:
        response = client.post("/signup", 
                                data={"email": "gru@minions.org",
                                      "password1": "12345678",
                                      "password2": "12345678"})

        #print("\n\n", response.data)
        assert response.status_code == 302 # redirect to home page
        assert b'Redirecting' in response.data

def test_success_login(client):

    response = client.get('/login')
    assert response.status_code == 200
    assert b'email' in response.data
    assert b'password' in response.data

    with client:
        response = client.post("/signup", 
                                data={"email": "gru@minions.org",
                                      "password1": "12345678",
                                      "password2": "12345678"})

        response = client.post("/login", 
                                data={"email": "gru@minions.org",
                                      "password": "12345678"})

        print("\n\n", response.data)
        assert response.status_code == 302 # redirect to home page
        assert b'Redirecting' in response.data 


def test_logout(client):

    with client:
        response = client.post("/signup", 
                                data={"email": "gru@minions.org",
                                      "password1": "12345678",
                                      "password2": "12345678"})

        response = client.post("/login", 
                                data={"email": "gru@minions.org",
                                      "password": "12345678"})

        response = client.get('/logout', follow_redirects=True)
        print("\n\n", response.data)
        #assert response.status_code == 302 # redirect to login page
        #assert b'Redirecting' in response.data

        #response = client.get('/', follow_redirects=True)
        assert response.status_code == 200
        assert b'login' in response.data