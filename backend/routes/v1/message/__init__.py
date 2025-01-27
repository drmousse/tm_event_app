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
    User,
    UserSession,
    Message
)
from interfaces import (
    create_message,
    get_messages_sorted_by,
    handle_message
)


# GLOBALS


# FUNCTIONS
def message_route_v():
    session_id = request.cookies.get('tio_session_id')
    frontend_data = request.get_json() if request.method == 'POST' else {}

    if session_id:
        user_session = UserSession.KeywordQuery(session_id=session_id.encode())[0]

        if user_session:
            if request.method == 'GET':
                pass

            elif request.method == 'POST':

                if not frontend_data.get('data'):
                    return make_response(jsonify({
                        'success': False,
                        'result': 'message/no-data',
                        'error': "Es wurden leider keine Daten übermittelt."
                    }), 200)

                user = User.GetUserByID(user_session.user_id)
                user_fullname = f'{user.firstname} {user.lastname}'
                content = frontend_data['data']['content']

                success, result, message = create_message(user.user_id, user_fullname, tioglobals.TIO_MESSAGE_GENERAL, content)

                return make_response(jsonify({
                    'success': success,
                    'result': result,
                    'message': message
                }), 200)

    return make_response(jsonify({
        'success': False,
        'result': 'auth/no-session',
        'message': 'Keine Sitzung gefunden'
    }), 200)


def get_messages_route_v():
    session_id = request.cookies.get('tio_session_id')
    frontend_data = request.get_json() if request.method == 'POST' else {}

    if session_id:
        user_session = UserSession.KeywordQuery(session_id=session_id.encode())[0]

        if user_session:
            if request.method == 'GET':
                pass

            elif request.method == 'POST':

                if not frontend_data.get('data'):
                    return make_response(jsonify({
                        'success': False,
                        'result': 'message/no-data',
                        'error': "Es wurden leider keine Daten übermittelt."
                    }), 200)

                user = User.GetUserByID(user_session.user_id)
                message_type = frontend_data['data']['messageType']

                success, messages, message = get_messages_sorted_by(message_type, sorted_by='created_on', reverse=True)

                if messages:
                    for message in messages.get('parent_messages'):
                        if message['user_id'] == user.user_id:
                            message['is_editable'] = True
                        else:
                            message['is_editable'] = False

                        if messages.get('sub_messages'):
                            sub_messages = messages['sub_messages'].get(message['message_id'])
                            if sub_messages:
                                for sub_message in sub_messages:
                                    if sub_message['user_id'] == user.user_id:
                                        sub_message['is_editable'] = True
                                    else:
                                        sub_message['is_editable'] = False

                return make_response(jsonify({
                    'success': success,
                    'result': messages,
                    'message': message
                }), 200)

    return make_response(jsonify({
        'success': False,
        'result': 'auth/no-session',
        'message': 'Keine Sitzung gefunden'
    }), 200)


def handle_message_route_v():
    session_id = request.cookies.get('tio_session_id')
    frontend_data = request.get_json() if request.method == 'POST' else {}

    if session_id:
        user_session = UserSession.KeywordQuery(session_id=session_id.encode())[0]

        if user_session:
            if request.method == 'GET':
                pass

            elif request.method == 'POST':

                if not frontend_data.get('data'):
                    return make_response(jsonify({
                        'success': False,
                        'result': 'message/no-data',
                        'error': "Es wurden leider keine Daten übermittelt."
                    }), 200)

                user = User.GetUserByID(user_session.user_id)
                success, result, message = handle_message(user, frontend_data['data'])

                return make_response(jsonify({
                    'success': success,
                    'result': result,
                    'message': message
                }), 200)

    return make_response(jsonify({
        'success': False,
        'result': 'auth/no-session',
        'message': 'Keine Sitzung gefunden'
    }), 200)