#!/usr/bin/python3
# -*- coding: utf-8 -*-

# core imports
import sqlalchemy
from datetime import datetime
from flask import request, jsonify, make_response

# custom imports
from apiversion import api_version
import tioglobals
from tools import parse_date, get_event_status_number
from models import (
    TioDB,
    GameStation,
    UserSession,
    User
)
from interfaces import (
    get_game_stations
)


# GLOBALS


# FUNCTIONS
def get_games_station_route_v():
    session_id = request.cookies.get('tio_session_id')
    frontend_data = request.get_json() if request.method == 'POST' else {}

    if session_id:
        user_session = UserSession.KeywordQuery(session_id=session_id.encode())[0]

        if user_session:
            if not frontend_data.get('eventId'):
                return make_response(jsonify({
                    'success': False,
                    'result': 'gamestation/no-event',
                    'error': "Es wurden leider keine Daten übermittelt."
                }), 200)

            event_id = frontend_data['eventId']
            success, result, message = get_game_stations(event_id, user_session.user_id)

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