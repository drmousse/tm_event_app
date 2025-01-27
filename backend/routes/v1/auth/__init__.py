#!/usr/bin/python3
# -*- coding: utf-8 -*-

# core imports
import sqlalchemy
from datetime import datetime
from timeit import default_timer as timer
from flask import request, jsonify, make_response

# custom imports
import tools
from apiversion import api_version
from models import (
    TioDB,
    User,
    UserSession,
    Games,
    UserSettings,
    EventFormat
)
from interfaces import (
    check_login,
    create_user_session_tokens,
    get_users_roles,

)

# GLOBALS
WAIT_DURATION_LOGIN = 2


# FUNCTIONS
def login_route_v():
    start = timer()
    if request.method == 'POST':
        frontend_data = request.get_json()
        user_login = frontend_data.get('login')
        password = frontend_data.get('password')
        if not (user_login and password):
            return jsonify({'result': 'auth/forms-not-filled'})

        user = User.ByKeys(user_login)
        if not user:
            tools.wait_time(start, WAIT_DURATION_LOGIN)
            return make_response(jsonify({
                'success': False,
                'result': 'auth/login-fail',
                'error': 'Benutzername oder Passwort falsch. Bitte erneut versuchen.'
            }), 200)

        if check_login(user, password) and int(user.active):
            refresh_token, access_token, session_id = create_user_session_tokens(user)
            games = Games.Query()
            user_settings = UserSettings.KeywordQuery(user_id=user.user_id)
            event_formats = EventFormat.Query()
            role_names = get_users_roles(user.user_id)

            response = make_response(jsonify({
                'result': 'auth/login-success',
                'tio_access_token': access_token.decode(),
                'tio_games': games,
                'tio_user_settings': user_settings,
                'tio_event_formats': event_formats,
                'tio_my_roles': role_names[user.user_id],
                'tio_user_data': {
                    'name': [user.firstname, user.lastname]
                },
                'tio_first_login': user.first_login
            }))

            # todo: hier max_age auf 8 Stunden setzen, sobald die App final getestet worden ist
            response.set_cookie(
                'tio_refresh_token',
                refresh_token.decode(),
                max_age=60*60*8,
                httponly=True,
                samesite='Lax',
                secure=True
            )
            response.set_cookie(
                'tio_session_id',
                session_id.decode(),
                max_age=60*60*12,
                httponly=True,
                samesite='Lax',
                secure=True
            )

            tools.wait_time(start, WAIT_DURATION_LOGIN)

            return response

        tools.wait_time(start, WAIT_DURATION_LOGIN)

        return make_response(jsonify({
            'success': False,
            'result': 'auth/login-fail',
            'error': 'Benutzername oder Passwort falsch. Bitte erneut versuchen.'
        }), 200)


def validate_access_token_route_v():
    dt = datetime.now()

    frontend_data = request.get_json() if request.method == 'POST' else {}
    access_token = frontend_data.get('tio_access_token')
    session_id = request.cookies.get('tio_session_id')
    refresh_token = request.cookies.get('tio_refresh_token')

    def not_auth():
        resp = make_response(jsonify({'result': 'auth/not-authorized'}), 401)
        resp.delete_cookie('tio_refresh_token')
        resp.delete_cookie('tio_session_id')
        resp.headers['Content-Type'] = 'application/json'
        return resp

    def full_auth():
        resp = make_response(jsonify({'result': 'auth/fully-authorized'}), 200)
        resp.headers['Content-Type'] = 'application/json'
        return resp

    def partial_auth():
        resp = make_response(jsonify({'result': 'auth/partially-authorized'}), 200)
        resp.headers['Content-Type'] = 'application/json'
        return resp

    # first of all we are going to check, if there is a session id.
    # session_id is a must. if there is no session_id, then the user
    # will be directed immediately to the login page
    if not session_id:
        print("No session ID, not authorized.")
        return not_auth()

    # if session_id exists, then there is an entry in database.
    # afterward we are going to check, if session is still valid
    user_session = UserSession.KeywordQuery(session_id=session_id.encode())[0]

    if request.method == 'GET':
        # if it's GET, then we can only check for the refresh_token
        if refresh_token:
            if user_session.refresh_token == refresh_token.encode():
                # todo: pruefen, ob token abgelaufen ist
                print("Refresh token is valid, partial auth.")
                return partial_auth()

        print("No valid refresh token, not authorized.")
        return not_auth()

    # if we get so far, the request method is POST
    if access_token:
        # todo: check if access_token is still valid
        return full_auth()

    if refresh_token:
        if refresh_token:
            if user_session.refresh_token == refresh_token.encode():
                # todo: pruefen, ob token abgelaufen ist
                return partial_auth()

    return not_auth()


def logout_route_v():
    response = make_response(jsonify({'success': True}), 200)
    response.set_cookie('tio_session_id', "", expires=0, httponly=True)
    response.set_cookie('tio_refresh_token', "", expires=0, httponly=True)

    return response

