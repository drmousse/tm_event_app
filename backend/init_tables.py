#!/usr/bin/python3
# -*- coding: utf-8 -*-


# imports
from models import TioDB, OLC, Roles, UserRoles, Games, EventFormat
from tools import generate_id
from interfaces import create_user

# globals
# functions
# classes


def init_olc():
    olcs = [
        OLC(status=0, type='event', color='white', name='Neu'),
        OLC(status=50, type='event', color='blue', name='Live'),
        OLC(status=100, type='event', color='green', name='Abgeschlossen'),
        OLC(status=180, type='event', color='grey', name='Verworfen'),
        OLC(status=0, type='game', color='white', name='Neu'),
        OLC(status=50, type='game', color='blue', name='Live'),
        OLC(status=100, type='game', color='green', name='Abgeschlossen'),
        OLC(status=180, type='game', color='grey', name='Verworfen'),
    ]
    TioDB.add_objects(olcs)


def init_roles():
    roles = [
        Roles(role_id=generate_id(Roles.__tablename__), type='CommonRole', name='Admin'),
        Roles(role_id=generate_id(Roles.__tablename__), type='CommonRole', name='User'),
        Roles(role_id=generate_id(Roles.__tablename__), type='CommonRole', name='Manager'),
        Roles(role_id=generate_id(Roles.__tablename__), type='CommonRole', name='Customer'),
        Roles(role_id=generate_id(Roles.__tablename__), type='EventRole', name='Event-Lead'),
        Roles(role_id=generate_id(Roles.__tablename__), type='EventRole', name='Event-Rocker'),
    ]
    TioDB.add_objects(roles)


def init_users():
    users = [
        ({'login': 'dietrich@teamio.de',
          'firstname': 'Johannes',
          'lastname': 'Dietrich',
          'email': 'dietrich@teamio.de',
          'gender': 'M',
          'title': 'Herr',
          'function': 'CEO',
          'active': 1,
          'first_login': 1},
         'dietrich',
         [{'role_id': 'TR000000000001'}, {'role_id': 'TR000000000002'}, {'role_id': 'TR000000000003'}]
         ),
        ({'login': 'lal@teamio.de',
          'firstname': 'Amit',
          'lastname': 'Lal',
          'email': 'lal@teamio.de',
          'gender': 'M',
          'title': 'Herr',
          'function': 'CEO',
          'active': 1,
          'first_login': 1},
         'lal',
         [{'role_id': 'TR000000000001'}, {'role_id': 'TR000000000002'}, {'role_id': 'TR000000000003'}]
         ),
        ({'login': 'dev@teamio.de',
          'firstname': 'Mousse',
          'lastname': 'T.',
          'email': 'dev@teamio.de',
          'gender': 'M',
          'title': 'Dr.',
          'function': 'CTO',
          'active': 1,
          'first_login': 0},
         'asdf',
         [{'role_id': 'TR000000000001'}, {'role_id': 'TR000000000002'}, {'role_id': 'TR000000000003'}]
         )
    ]

    for user, pw, roles in users:
        new_user, _, _ = create_user(user, pw, roles)


def init_games():
    games = [
        Games(game_id=generate_id(Games.__tablename__), name='Quiz Show', description='', score_type='Punkte', score_counting='Aufsteigend', duration=20, active=1),
        Games(game_id=generate_id(Games.__tablename__), name='Mario Kart', description='', score_type='Punkte', score_counting='Aufsteigend', duration=20, active=1),
        Games(game_id=generate_id(Games.__tablename__), name='Eisstockschießen', description='', score_type='Punkte', score_counting='Aufsteigend', duration=20, active=1),
        Games(game_id=generate_id(Games.__tablename__), name='Bogenschießen', description='', score_type='Punkte', score_counting='Aufsteigend', duration=20, active=1),
        Games(game_id=generate_id(Games.__tablename__), name='Laddergolf', description='', score_type='Punkte', score_counting='Aufsteigend', duration=20, active=1),
        Games(game_id=generate_id(Games.__tablename__), name='Dart-Turnier', description='', score_type='Punkte', score_counting='Aufsteigend', duration=20, active=1)
    ]
    TioDB.add_objects(games)


def init_event_formats():
    event_format = [
        EventFormat(format_id=generate_id(EventFormat.__tablename__), name='Bauernhof Rallye'),
        EventFormat(format_id=generate_id(EventFormat.__tablename__), name='Beach Games'),
        EventFormat(format_id=generate_id(EventFormat.__tablename__), name='Bogenschießen'),
        EventFormat(format_id=generate_id(EventFormat.__tablename__), name='Business Yoga'),
        EventFormat(format_id=generate_id(EventFormat.__tablename__), name='Cajón-Workshop'),
        EventFormat(format_id=generate_id(EventFormat.__tablename__), name='Casino Night'),
        EventFormat(format_id=generate_id(EventFormat.__tablename__), name='Crossgolf Experience'),
        EventFormat(format_id=generate_id(EventFormat.__tablename__), name='Dart-Turnier'),
        EventFormat(format_id=generate_id(EventFormat.__tablename__), name='Digitaler 3-Kampf'),
        EventFormat(format_id=generate_id(EventFormat.__tablename__), name='Domino Effekt'),
        EventFormat(format_id=generate_id(EventFormat.__tablename__), name='Drachenboot Festival'),
        EventFormat(format_id=generate_id(EventFormat.__tablename__), name='Drone Race'),
        EventFormat(format_id=generate_id(EventFormat.__tablename__), name='Drum Event'),
        EventFormat(format_id=generate_id(EventFormat.__tablename__), name='Eisstockschießen'),
        EventFormat(format_id=generate_id(EventFormat.__tablename__), name='Fackel-Bogenschießen'),
        EventFormat(format_id=generate_id(EventFormat.__tablename__), name='Feierabend BINGO Show'),
        EventFormat(format_id=generate_id(EventFormat.__tablename__), name='Firmen-Weihnachtsmarkt'),
        EventFormat(format_id=generate_id(EventFormat.__tablename__), name='fit@work'),
        EventFormat(format_id=generate_id(EventFormat.__tablename__), name='Floßbau Teamevent'),
        EventFormat(format_id=generate_id(EventFormat.__tablename__), name='Glühwein Expedition'),
        EventFormat(format_id=generate_id(EventFormat.__tablename__), name='GPS-Rallye'),
        EventFormat(format_id=generate_id(EventFormat.__tablename__), name='Hotel- und Bürogolf'),
        EventFormat(format_id=generate_id(EventFormat.__tablename__), name='Human Table Soccer'),
        EventFormat(format_id=generate_id(EventFormat.__tablename__), name="Hütt'n Challenge"),
        EventFormat(format_id=generate_id(EventFormat.__tablename__), name='Indoor Team-Parcours'),
        EventFormat(format_id=generate_id(EventFormat.__tablename__), name='Insektenhotelbau-Event'),
        EventFormat(format_id=generate_id(EventFormat.__tablename__), name='iPad Rallye'),
        EventFormat(format_id=generate_id(EventFormat.__tablename__), name='Kicker Cup'),
        EventFormat(format_id=generate_id(EventFormat.__tablename__), name='Kickerbau-Event'),
        EventFormat(format_id=generate_id(EventFormat.__tablename__), name='Koch-Event'),
        EventFormat(format_id=generate_id(EventFormat.__tablename__), name='Kreativ-Werkstatt'),
        EventFormat(format_id=generate_id(EventFormat.__tablename__), name='Kreativ-Werkstatt @home'),
        EventFormat(format_id=generate_id(EventFormat.__tablename__), name='Kurzfilm Gala'),
        EventFormat(format_id=generate_id(EventFormat.__tablename__), name='Live Escape Game'),
        EventFormat(format_id=generate_id(EventFormat.__tablename__), name='Mario Kart-Event'),
        EventFormat(format_id=generate_id(EventFormat.__tablename__), name='Online Drum-Event'),
        EventFormat(format_id=generate_id(EventFormat.__tablename__), name='Online Escape Game'),
        EventFormat(format_id=generate_id(EventFormat.__tablename__), name='Online Gin Tasting'),
        EventFormat(format_id=generate_id(EventFormat.__tablename__), name='Online Pub Quiz & Craft Beer-Tasting'),
        EventFormat(format_id=generate_id(EventFormat.__tablename__), name='Online Quiz Show'),
        EventFormat(format_id=generate_id(EventFormat.__tablename__), name='Online Schokoladen-Workshop'),
        EventFormat(format_id=generate_id(EventFormat.__tablename__), name='Online Wine Tasting'),
        EventFormat(format_id=generate_id(EventFormat.__tablename__), name='Quiz Show'),
        EventFormat(format_id=generate_id(EventFormat.__tablename__), name='Rasencurling'),
        EventFormat(format_id=generate_id(EventFormat.__tablename__), name='Remote Domino-Kettenreaktion'),
        EventFormat(format_id=generate_id(EventFormat.__tablename__), name='Segway Expedition'),
        EventFormat(format_id=generate_id(EventFormat.__tablename__), name='Seifenkisten Derby'),
        EventFormat(format_id=generate_id(EventFormat.__tablename__), name='teamio 3-Kampf'),
        EventFormat(format_id=generate_id(EventFormat.__tablename__), name='teamio 5-Kampf'),
        EventFormat(format_id=generate_id(EventFormat.__tablename__), name='teamio Biathlon'),
        EventFormat(format_id=generate_id(EventFormat.__tablename__), name='Team-Parcours'),
        EventFormat(format_id=generate_id(EventFormat.__tablename__), name='Virtuelles Koch Event'),
        EventFormat(format_id=generate_id(EventFormat.__tablename__), name='Weihnachtsbäckerei'),
        EventFormat(format_id=generate_id(EventFormat.__tablename__), name='Weihnachtsbäckerei Online'),
        EventFormat(format_id=generate_id(EventFormat.__tablename__), name='Weihnachtsgolf-Turnier'),
        EventFormat(format_id=generate_id(EventFormat.__tablename__), name='Weihnachtsmarkt Rallye'),
        EventFormat(format_id=generate_id(EventFormat.__tablename__), name='Xmas Quiz Show')
    ]
    TioDB.add_objects(event_format)


def init_tables():
    init_olc()
    init_roles()
    init_users()
    init_games()
    init_event_formats()


if __name__ == '__main__':
    with TioDB.app.app_context():
        TioDB.db.drop_all()
        TioDB.db.create_all()
        init_tables()
