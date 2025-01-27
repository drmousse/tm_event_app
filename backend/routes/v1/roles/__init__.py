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
    get_roles
)


# FUNCTIONS
def get_all_roles_route_v():
    session_id = request.cookies.get('tio_session_id')
    frontend_data = request.get_json() if request.method == 'POST' else {}

    if session_id:
        user_session = UserSession.KeywordQuery(session_id=session_id.encode())[0]
        if user_session:
            role_type = frontend_data.get('roleType')
            success, result, error = get_roles(role_type)

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
