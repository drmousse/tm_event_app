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
    Roles,
    UserSession
)

from interfaces import (
    get_event_game_comment,
    set_event_game_comment
)


# FUNCTIONS
def get_event_game_comment_route_v():
    session_id = request.cookies.get('tio_session_id')
    frontend_data = request.get_json() if request.method == 'POST' else {}

    if session_id:
        user_session = UserSession.KeywordQuery(session_id=session_id.encode())[0]
        if user_session:
            if not frontend_data.get('data'):
                return make_response(jsonify({
                    'success': False,
                    'result': 'eventscore/no-data',
                    'error': "Es wurden leider keine Daten übermittelt."
                }), 200)

            event_id = frontend_data['data']['eventId']
            game_id = frontend_data['data']['gameId']
            success, result, message = get_event_game_comment(event_id, game_id)

            return make_response(jsonify({
                'success': success,
                'result': result,
                'message': message
            }), 200)

        return make_response(jsonify({
            'success': False,
            'result': 'auth/no-session',
            'message': 'Keine Sitzung gefunden'
        }))


def set_event_game_comment_route_v():
    session_id = request.cookies.get('tio_session_id')
    frontend_data = request.get_json() if request.method == 'POST' else {}

    if session_id:
        user_session = UserSession.KeywordQuery(session_id=session_id.encode())[0]
        if user_session:
            if not frontend_data.get('data'):
                return make_response(jsonify({
                    'success': False,
                    'result': 'eventscore/no-data',
                    'error': "Es wurden leider keine Daten übermittelt."
                }), 200)

            event_id = frontend_data['data']['eventId']
            game_id = frontend_data['data']['gameId']
            comment = frontend_data['data']['comment']
            success, result, message = set_event_game_comment(event_id, game_id, comment)

            return make_response(jsonify({
                'success': success,
                'result': result,
                'message': message
            }), 200)

        return make_response(jsonify({
            'success': False,
            'result': 'auth/no-session',
            'message': 'Keine Sitzung gefunden'
        }))
