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
    update_teams_names
)


# FUNCTIONS
def update_teams_names_route_v():
    session_id = request.cookies.get('tio_session_id')
    frontend_data = request.get_json() if request.method == 'POST' else {}

    if session_id:
        user_session = UserSession.KeywordQuery(session_id=session_id.encode())[0]

        if user_session:
            if request.method == 'GET':
                # at the moment no need to just get the team names. but who knows.
                pass
            else:
                teams = frontend_data['teams']
                success, result, message = update_teams_names(teams)

                return make_response(jsonify({
                    'success': success,
                    'result': result,
                    'message': message
                }))


    return make_response(jsonify({
        'success': False,
        'result': 'auth/no-session',
        'message': 'Keine Sitzung gefunden'
    }))
