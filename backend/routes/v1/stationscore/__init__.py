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
    update_station_scores,
    get_station_team_placements
)


# FUNCTIONS
def update_station_score_route_v():
    session_id = request.cookies.get('tio_session_id')
    frontend_data = request.get_json() if request.method == 'POST' else {}

    if session_id:
        user_session = UserSession.KeywordQuery(session_id=session_id.encode())[0]
        if user_session:
            event_id = frontend_data.get('eventId')
            team_scores = frontend_data.get('teamScores')

            success, result, error = update_station_scores(event_id, team_scores)

            return make_response(jsonify({
                'success': success,
                'result': result,
                'error': error
            }), 200)
    else:
        return make_response(jsonify({
            'success': False,
            'result': 'auth/not-authorized',
            'error': "No session found"
        }), 200)


def get_station_team_placements_route_v():
    session_id = request.cookies.get('tio_session_id')
    frontend_data = request.get_json() if request.method == 'POST' else {}

    if session_id:
        user_session = UserSession.KeywordQuery(session_id=session_id.encode())[0]
        if user_session:
            event_id = frontend_data.get('eventId')
            game_id = frontend_data.get('gameId')

            success, result, error = get_station_team_placements(event_id, game_id)

            return make_response(jsonify({
                'success': success,
                'result': result,
                'error': error
            }), 200)
    else:
        return make_response(jsonify({
            'success': False,
            'result': 'auth/not-authorized',
            'error': "No session found"
        }), 200)
