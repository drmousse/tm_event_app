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
    UserSession,
    UserRoles
)

from interfaces import (
    get_users_roles
)


# FUNCTIONS
def get_my_roles_route_v():
    session_id = request.cookies.get('tio_session_id')

    if session_id:
        user_session = UserSession.KeywordQuery(session_id=session_id.encode())[0]
        if user_session:
            # todo: refactoren, sodass get_users_roles, succes, result und error zurückgibt
            roles = get_users_roles(user_session.user_id)

            return make_response(jsonify({'success': True, 'result': roles[user_session.user_id], 'error': None}), 200)
    else:
        return make_response(jsonify({
            'success': False,
            'result': 'auth/not-authorized',
            'error': "No session found"
        }), 200)


def get_users_roles_route_v():
    session_id = request.cookies.get('tio_session_id')
    frontend_data = request.get_json() if request.method == 'POST' else {}

    if session_id:
        user_session = UserSession.KeywordQuery(session_id=session_id.encode())[0]
        if user_session:
            user_ids = frontend_data.get('user_ids')
            user_roles = get_users_roles(user_ids)

            # todo: refactoren, sodass get_users_roles, succes, result und error zurückgibt
            if user_roles:
                return make_response(jsonify({
                    'success': True,
                    'result': user_roles,
                    'error': None
                }))
            else:
                return make_response(jsonify({
                    'success': False,
                    'result': 'userroles/no-roles',
                    'error': "Es wurden keine Rollen gefunden"
                }))
    # todo: sich um die else-fälle kümmern
