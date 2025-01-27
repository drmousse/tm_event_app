#!/usr/bin/python3
# -*- coding: utf-8

# core imports
import importlib

# custom imports
from models import TioDB
from apiversion import api_version

routes = importlib.import_module(f'routes.{api_version}')
games = importlib.import_module(f'routes.{api_version}.games')
events = importlib.import_module(f'routes.{api_version}.events')
auth = importlib.import_module(f'routes.{api_version}.auth')
eventformats = importlib.import_module(f'routes.{api_version}.eventformats')
users = importlib.import_module(f'routes.{api_version}.users')
usersettings = importlib.import_module(f'routes.{api_version}.usersettings')
roles = importlib.import_module(f'routes.{api_version}.roles')
userroles = importlib.import_module(f'routes.{api_version}.userroles')
gamestation = importlib.import_module(f'routes.{api_version}.gamestation')
team = importlib.import_module(f'routes.{api_version}.team')
stationscore = importlib.import_module(f'routes.{api_version}.stationscore')
message = importlib.import_module(f'routes.{api_version}.message')
eventscore = importlib.import_module(f'routes.{api_version}.eventscore')
eventgamecomment = importlib.import_module(f'routes.{api_version}.eventgamecomment')


# routes
##########################################
# AUTH
##########################################
@TioDB.app.route(f'/api/login', methods=['POST'])
def login_route():
    return auth.login_route_v()


@TioDB.app.route(f'/api/{api_version}/validate_access', methods=['GET', 'POST'])
def validate_access_token_route():
    return auth.validate_access_token_route_v()


@TioDB.app.route(f'/api/logout', methods=['GET'])
def logout_route():
    return auth.logout_route_v()


##########################################
# API
##########################################
@TioDB.app.route(f'/api', methods=['GET'])
def get_api_version():
    return routes.get_api_version_route_v()


##########################################
# EVENTS
##########################################
@TioDB.app.route(f'/api/{api_version}/event', methods=['POST'])
def get_event_route():
    return events.get_event_route_v()


@TioDB.app.route(f'/api/{api_version}/event/status', methods=['POST'])
def set_event_status_route():
    return events.set_event_status_route_v()


@TioDB.app.route(f'/api/{api_version}/create/event', methods=['POST'])
def create_event_route():
    return events.create_event_route_v()


@TioDB.app.route(f'/api/{api_version}/events', methods=['POST'])
def get_events_route():
    return events.get_events_route_v()


@TioDB.app.route(f'/api/{api_version}/events/upcoming', methods=['GET'])
def get_upcoming_events_route():
    return events.get_upcoming_events_route_v()


##########################################
# EVENTFORMAT
##########################################
@TioDB.app.route(f'/api/{api_version}/eformats', methods=['GET'])
def get_all_event_formats():
    return eventformats.get_all_event_formats_route_v()


##########################################
# EVENTSCORE
##########################################
@TioDB.app.route(f'/api/{api_version}/eventscore/gamestation/update', methods=['POST'])
def update_event_score_by_gamestation_route():
    return eventscore.update_event_score_by_gamestation_route_v()


@TioDB.app.route(f'/api/{api_version}/eventscore/update', methods=['POST'])
def update_event_score_route():
    """
    Updating single event score
    :return:
    """
    return eventscore.update_event_score_route_v()


@TioDB.app.route(f'/api/{api_version}/eventscores/update', methods=['POST'])
def update_event_scores_route():
    """
    Updating multiple event scores
    :return:
    """
    return eventscore.update_event_scores_route_v()


##########################################
# EVENTGAMECOMMENT
##########################################
@TioDB.app.route(f'/api/{api_version}/eventgamecomment', methods=['POST'])
def get_event_game_comment_route():
    return eventgamecomment.get_event_game_comment_route_v()


@TioDB.app.route(f'/api/{api_version}/eventgamecomment/update', methods=['POST'])
def set_event_game_comment_route():
    return eventgamecomment.set_event_game_comment_route_v()


##########################################
# MESSAGE
##########################################
@TioDB.app.route(f'/api/{api_version}/message', methods=['GET', 'POST'])
def message_route():
    return message.message_route_v()


@TioDB.app.route(f'/api/{api_version}/messages', methods=['GET', 'POST'])
def get_messages_route():
    return message.get_messages_route_v()


@TioDB.app.route(f'/api/{api_version}/message/multihandle', methods=['POST'])
def handle_message_route():
    return message.handle_message_route_v()


##########################################
# GAMES
##########################################
@TioDB.app.route(f'/api/{api_version}/create/game', methods=['POST'])
def create_game_route():
    return games.create_game_route_v()


@TioDB.app.route(f'/api/{api_version}/games', methods=['GET', 'POST'])
def get_all_games_route():
    return games.get_all_games_route_v()


@TioDB.app.route(f'/api/{api_version}/games/status', methods=['POST'])
def set_game_status_route():
    return games.set_game_status_route_v()


@TioDB.app.route(f'/api/{api_version}/games/update', methods=['POST'])
def update_game_route():
    return games.update_game_route_v()


##########################################
# GAMES
##########################################
@TioDB.app.route(f'/api/{api_version}/gamestation', methods=['POST'])
def get_games_station_route():
    return gamestation.get_games_station_route_v()


##########################################
# USERS
##########################################
@TioDB.app.route(f'/api/{api_version}/users', methods=['GET', 'POST'])
def get_all_users_route():
    return users.get_all_users_route_v()


@TioDB.app.route(f'/api/{api_version}/create/user', methods=['POST'])
def create_user_route():
    return users.create_user_route_v()


@TioDB.app.route(f'/api/{api_version}/user/mydata', methods=['GET'])
def get_mydata_route():
    return users.get_mydata_route_v()


@TioDB.app.route(f'/api/{api_version}/user/updatedata', methods=['POST'])
def update_mydata_route():
    return users.update_mydata_route_v()


@TioDB.app.route(f'/api/{api_version}/user/firstlogin', methods=['GET', 'POST'])
def user_first_login_route():
    return users.user_first_login_route_v()


@TioDB.app.route(f'/api/{api_version}/user/changepw', methods=['POST'])
def user_change_password_route():
    return users.user_change_password_route_v()


@TioDB.app.route(f'/api/{api_version}/user/update', methods=['POST'])
def update_user_route():
    return users.update_user_route_v()


@TioDB.app.route(f'/api/{api_version}/user/password', methods=['POST'])
def update_user_password_route():
    return users.update_user_password_route_v()


# todo: get und post separieren, da der name der methode sonst irreführend ist
@TioDB.app.route(f'/api/{api_version}/user/status', methods=['GET', 'POST'])
def set_user_account_status_route():
    return users.set_user_account_status_route_v()


##########################################
# USER SETTINGS
##########################################
@TioDB.app.route(f'/api/{api_version}/user/settings', methods=['POST'])
def user_settings_route():
    return usersettings.user_settings_route_v()


##########################################
# USER ROLES
##########################################
@TioDB.app.route(f'/api/{api_version}/userroles/myroles', methods=['GET'])
def get_my_roles_route():
    return userroles.get_my_roles_route_v()


@TioDB.app.route(f'/api/{api_version}/userroles', methods=['POST'])
def get_users_roles_route():
    return userroles.get_users_roles_route_v()


##########################################
# BLOBSTORE
##########################################
@TioDB.app.route(f'/api/{api_version}/upload', methods=['POST'])
def upload_blob_route():
    return routes.upload_blob_route_v()


##########################################
# ROLES
##########################################
@TioDB.app.route(f'/api/{api_version}/roles', methods=['POST'])
def get_all_roles_route():
    return roles.get_all_roles_route_v()


##########################################
# ABOUT
##########################################
@TioDB.app.route(f'/api/{api_version}/about', methods=['GET'])
def get_app_information_route():
    return routes.get_app_information_route_v()


##########################################
# TEAM
##########################################
@TioDB.app.route(f'/api/{api_version}/teams/names', methods=['GET', 'POST'])
def update_teams_names_route():
    return team.update_teams_names_route_v()


##########################################
# STATIONSCORE
##########################################
@TioDB.app.route(f'/api/{api_version}/stationscore/update', methods=['POST'])
def update_station_score_route():
    return stationscore.update_station_score_route_v()


@TioDB.app.route(f'/api/{api_version}/stationscore/placement', methods=['POST'])
def get_station_team_placements_route():
    return stationscore.get_station_team_placements_route_v()


if __name__ == '__main__':
    TioDB.run()
