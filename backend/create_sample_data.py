#!/usr/bin/python3
# -*- coding: utf-8 -*-


# imports
from models import TioDB, Event, Games, UserRoles
from tools import generate_id
from interfaces import create_user

# globals
# functions
# classes


# todo: create samples noch fertig stellen
def create_sample_users():
    users = [
        ({"login": "test@teamio.de", "firstname": "Dummy", "lastname": "User", "email": "dummy@teamio.de", "gender": "M", "title": "Herr", "function": "Angestellter", "active": 1, 'first_login': 1}, "asdf")
    ]

    for user, pw in users:
        new_user, new_user_pw = create_user(user, pw)
        TioDB.add_objects([new_user, new_user_pw])


def create_sample_user_roles():
    user_roles = [
        UserRoles(user_id='TU000000000004', role_id='TR000000000002')
    ]
    TioDB.add_objects(user_roles)


def create_sample_data():
    create_sample_users()
    create_sample_user_roles()


if __name__ == '__main__':
    with TioDB.app.app_context():
        create_sample_data()
