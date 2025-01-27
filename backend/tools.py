#!/usr/bin/python3
# -*- coding: utf-8 -*-

# core imports
import bcrypt
import random
from datetime import datetime
from dateutil import parser
from collections import defaultdict
from timeit import default_timer as timer

# custom imports
import tioglobals
from models import TioDB, Counter
from api import (
    PW_STRING
)


# functions
def generate_id(table_name):
    """
        This function returns a table specific 12 character long string,
        e.g. for User table -> TU0000000001
    """
    match table_name:
        case 'tio_user':
            pre_fix = 'TU'
        case 'tio_roles':
            pre_fix = 'TR'
        case 'tio_event':
            pre_fix = 'TE'
        case 'tio_games':
            pre_fix = 'TG'
        case 'tio_game_station':
            pre_fix = 'TGS'
        case 'tio_team':
            pre_fix = 'TT'
        case 'tio_event_format':
            pre_fix = 'TEF'
        case 'tio_blobstore':
            pre_fix = 'TB'
        case 'tio_station_score':
            pre_fix = 'TSS'
        case 'tio_message':
            pre_fix = 'TM'
        case _:
            pre_fix = 'GEN'

    value = 1

    table_name_counter = Counter.query.get(table_name)
    if table_name_counter:
        value = table_name_counter.value + 1
        table_name_counter.value = value

    else:
        counter = Counter(counter_name=table_name, value=value)
        TioDB.db.session.add(counter)

    ret_id = f'{pre_fix}{value:0>{tioglobals.LENGTH_ID}}'
    TioDB.db.session.commit()
    return ret_id


# todo: funktion zu einer methode der UserSession machen oder in die model_functions
def create_user_session_id(user, dt):
    return bcrypt.hashpw(f'{user.user_id}-{dt}-{user.login}'.encode(), bcrypt.gensalt())


def parse_date(date_string):
    """
    Converts a date string into a datetime object.

    Parameters:
    date_string (str): The date string to convert.

    Returns:
    datetime: The corresponding datetime object.
    """
    try:
        return parser.parse(date_string)
    except (ValueError, TypeError) as e:
        # todo: durch logging ersetzen
        print(f"Error parsing date string: {e}")
        return None


def hash_pw(password):
    return bcrypt.hashpw(PW_STRING.format(password).encode(), bcrypt.gensalt())


def generate_team_game_comps(num_games, num_team):
    random.seed(int(datetime.now().timestamp()))
    # todo: folgenden code umsetzen
    #   idee ist, dass ich einfach per zufall von oben nach unten den teams games
    #   und gegner gebe, aber auch darauf achte, beim gegner entsprechend das team
    #   als auch das spiel wegzunehmen.
    #   beispiel: team1 spielt g2 gegen team4 -> setze für team4 als spiel g2 gegen team 1
    #   und so wird verfahren, bis alle teams keine spiele mehr haben
    #   am besten in jupyter weiter testen
    t = {
        'team1': {
            'games': ['g1', 'g2', 'g3'],
            'oppo': ['team2', 'team3', 'team4', 'team5', 'team6']
        },
        'team2': {
            'games': ['g1', 'g2', 'g3'],
            'oppo': ['team1', 'team3', 'team4', 'team5', 'team6']
        },
        'team3': {
            'games': ['g1', 'g2', 'g3'],
            'oppo': ['team2', 'team1', 'team4', 'team5', 'team6']
        },
        'team4': {
            'games': ['g1', 'g2', 'g3'],
            'oppo': ['team2', 'team3', 'team1', 'team5', 'team6']
        },
        'team5': {
            'games': ['g1', 'g2', 'g3'],
            'oppo': ['team2', 'team3', 'team4', 'team1', 'team6']
        },
        'team6': {
            'games': ['g1', 'g2', 'g3'],
            'oppo': ['team2', 'team3', 'team4', 'team5', 'team1']
        },
    }

    team_games = defaultdict(list)
    teams = ['team1', 'team2', 'team3', 'team4', 'team5', 'team6']
    for team1 in teams:
        print("team-durchlauf:", team1)
        f_cond = True
        counter = 1
        while f_cond:
            print('j')
            # schon mal im vorfeld checken, denn ggf. hat das team auch durch die schleifendurchlaeufe vorher
            # gar keine games mehr
            if len(t[team1]['games']):
                game_pos = random.randint(0, len(t[team1]['games']) - 1)
                team2_pos = random.randint(0, len(t[team1]['oppo']) - 1)
                print("game_pos, team2_pos:", game_pos, team2_pos)
                team_games[team].append(f"{t[team1]['games'][game_pos]}-{t[team1]['oppo'][rand_enemy_pos]}")
        
                # hier hole ich mir die namen der spiele und gegnerischen teams, die gegen 'team' antreten
                team2 = t[team1]['oppo'][rand_enemy_pos]
                game_name = t[team1]['games'][game_pos]
                print("team2, game_name:", team2, game_name)
        
                # hier werden die position des spiels in enemy team datenstruktur und position von 'team' geholt
                game_pos_in_team2 = t[team2]['games'].index(game_name)
                team1_pos_in_team2 = t[team2]['oppo'].index(team1)
        
                team_games[team2].append(f"{t[team2]['games'][game_pos_in_team2]}-{t[team2]['oppo'][team1_pos_in_team2]}")
                
                del t[team1]['games'][game_pos]
                del t[team1]['oppo'][team2_pos]
        
                del t[team2]['games'][game_pos_in_team2]
                del t[team2]['oppo'][team1_pos_in_team2]
                
                if not len(t[team1]['games']):
                    f_cond = False
                
                print(team1, t[team1])
                print(team2, t[team2])
                print("\n")
                print("\n")
            counter += 1

    print(team_games)


def get_media_type(request_file):
    file = request_file.get('tio_file/profile')
    if file:
        return file, 'profile'

    file = request_file.get('tio_file/event')
    if file:
        return file, 'event'

    file = request_file.get('tio_file/challenge')
    if file:
        return file, 'challenge'

    file = request_file.get('tio_file/customer')
    if file:
        return file, 'customer'

    return None, None


def get_event_status_number(status_name):
    name_to_number = {
        'new': 0,
        'active': 50,
        'closed': 100
    }

    return name_to_number.get(status_name)


def wait_time(start, wait_duration):
    """
    function which just waits for a given period of time beginning from start point.
    this prevents a time attack where an attacker gains information about validity of login existince
    by measuring the time of login process
    :param start:
    :param wait_duration:
    :return: None
    """
    while timer() - start < wait_duration:
        pass
