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
    update_event_score_by_gamestation,
    update_event_score,
    update_event_scores
)


# FUNCTIONS
def update_event_score_by_gamestation_route_v():
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
            success, result, message = update_event_score_by_gamestation(event_id)

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


def update_event_score_route_v():
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
            team_id = frontend_data['data']['teamId']
            score = frontend_data['data']['score']
            success, result, message = update_event_score(event_id, team_id, score)

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


def update_event_scores_route_v():
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
            event_scores = frontend_data['data']['eventScores']
            success, result, message = update_event_scores(event_id, event_scores)

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