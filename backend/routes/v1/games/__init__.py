#!/usr/bin/python3
# -*- coding: utf-8 -*-

# core imports
import sqlalchemy
from datetime import datetime
from flask import request, jsonify, make_response

# custom imports
from apiversion import api_version
from models import (
    TioDB,
    Games,
    UserSession
)
from interfaces import (
    create_game,
    update_blob_w_object_id,
    get_all_games,
    change_game_status,
    get_my_blob_name,
    update_game
)

# GLOBALS


# FUNCTIONS
def create_game_route_v():
    # todo: checken, ob das game schon existiert
    frontend_data = request.get_json() if request.method == 'POST' else {}
    new_game = {
        'name': frontend_data.get('gameName'),
        'description': frontend_data.get('gameDescription'),
        'score_type': frontend_data.get('selectedScoreType')['name'],
        'score_counting': frontend_data.get('selectedScoreCounting')['name'],
        'duration': frontend_data.get('gameDuration'),
        'game_blob_id': frontend_data.get('gamesBlobId'),
        'active': 1
    }
    blob_id = frontend_data.get('gamePictureBlobId')
    blob_upload_date = frontend_data.get('gamePictureBlobUploadDate')

    new_game, error_code, error_msg = create_game(new_game)

    if not new_game:
        # todo: anhand der fehlercodes entsprechende protokollierung durchfuehren
        if error_code == 'db_error':
            pass
        elif error_code == 'unknown_error':
            pass
        return make_response(jsonify({'success': False, 'result': error_code, 'error': error_msg}), 200)

    blob_update = update_blob_w_object_id(blob_id, new_game.game_id, blob_upload_date, 'media/game')

    return make_response(jsonify({
        'success': True,
        'result': 'game/creation-success',
        'blob_update': blob_update
    }), 200)


def get_all_games_route_v():
    session_id = request.cookies.get('tio_session_id')
    frontend_data = request.get_json() if request.method == 'POST' else {}

    if session_id:
        success, games, message = get_all_games()

        if request.method == 'POST':
            if frontend_data.get('options'):
                for option in frontend_data['options']:
                    match option:
                        case 'withProfilePhoto':
                            for game in games:
                                game['profilePhoto'] = get_my_blob_name(game.get('gameBlobId'))
                        case '_':
                            pass  # for now, no default use case

        return make_response(jsonify({
            'success': success,
            'result': games,
            'message': message
        }), 200)

    return make_response(jsonify({
        'success': False,
        'result': 'auth/no-session',
        'message': 'Keine Sitzung gefunden'
    }))


def set_game_status_route_v():
    session_id = request.cookies.get('tio_session_id')
    frontend_data = request.get_json() if request.method == 'POST' else {}

    if session_id:
        user_session = UserSession.KeywordQuery(session_id=session_id.encode())[0]

        if user_session:
            if not frontend_data:
                return make_response(jsonify({
                    'success': False,
                    'result': 'user/no-data',
                    'error': "Es wurden leider keine Daten übermittelt."
                }), 200)

            game_name = frontend_data.get('gameName')
            game_status = int(frontend_data.get('gameStatus'))
            user = Games.ByKeys(game_name)
            success, result, error = change_game_status(user, game_status)

            return make_response(jsonify({
                'success': success,
                'result': result,
                'error': error
            }), 200)

        return make_response(jsonify({
            'success': False,
            'result': 'auth/no-session',
            'message': 'Keine Sitzung gefunden'
        }))


def update_game_route_v():
    # todo: diese methode und update_mydata_route_v zu einer vereinen
    session_id = request.cookies.get('tio_session_id')
    frontend_data = request.get_json() if request.method == 'POST' else {}

    if session_id:
        user_session = UserSession.KeywordQuery(session_id=session_id.encode())[0]
        if user_session:
            if not frontend_data:
                return make_response(jsonify({
                    'success': False,
                    'result': 'game/no-data',
                    'error': "No data found."
                }), 200)

            game = Games.ByKeys(frontend_data.get('name'))

            success, result, error = update_game(game, frontend_data)

            return make_response(jsonify({
                'success': success,
                'result': result,
                'error': error
            }))

    else:
        # todo hier statt 200, 401 returnen und im frontend entsprechend reagieren
        return make_response(jsonify({
            'success': False,
            'result': 'auth/not-authorized',
            'error': "No session found"
        }), 200)

