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
    User,
    Blobstore,
    UserSession,
    UserPW
)
from interfaces import (
    check_user_exist,
    create_user,
    update_blob_w_object_id,
    update_user,
    get_user_object,
    check_login,
    update_user_pw,
    remove_first_login_flag,
    get_my_blob_name,
    get_users_roles,
    change_user_account_status
)

# GLOBALS


# FUNCTIONS
def create_user_route_v():
    # todo: jsonify durch make_response ersetzen. siehe login
    # todo: diesen route noch finalisieren. ist noch nicht vollstaendig. siehe frontendcode
    if request.method == 'POST':
        frontend_data = request.get_json() if request.method == 'POST' else {}
        new_user = {
            'login': frontend_data.get('login'),
            'firstname': frontend_data.get('firstname'),
            'lastname': frontend_data.get('lastname'),
            'pw_last_changed': datetime.now(),
            'phone': frontend_data.get('phone'),
            'gender': frontend_data.get('gender'),
            'title': frontend_data.get('title'),
            'function': frontend_data.get('function'),
            'email': frontend_data.get('email'),
            'profile_blob_id': frontend_data.get('profileBlobId'),
            'active': 1,
            'first_login': 1
        }
        user_roles = frontend_data.get('userroles')
        password = frontend_data.get('password')
        blob_id = frontend_data.get('userProfilePictureBlobId')
        blob_upload_date = frontend_data.get('userProfilePictureBlobUploadDate')

        if check_user_exist(new_user.get('login')):
            return make_response(jsonify({'success': False, 'result': 'user/already-exists'}), 200)

        new_user, error_code, error_msg = create_user(new_user, password, user_roles)

        if not new_user:
            # todo: anhand der fehlercodes entsprechende protokollierung durchfuehren
            if error_code == 'db_error':
                pass
            elif error_code == 'unknown_error':
                pass
            return make_response(jsonify({'success': False, 'result': error_code, 'error': error_msg}), 200)

        blob_update = update_blob_w_object_id(blob_id, new_user.user_id, blob_upload_date, 'media/user')

        return make_response(jsonify({
            'success': True,
            'result': 'user/creation-success',
            'blob_update': blob_update
        }), 200)


def get_all_users_route_v():
    session_id = request.cookies.get('tio_session_id')
    all_users = User.Query()
    frontend_data = request.get_json() if request.method == 'POST' else {}

    if session_id:
        if all_users:
            if request.method == 'POST':
                if frontend_data.get('options'):
                    for option in frontend_data['options']:
                        match option:
                            case 'withProfilePhoto':
                                for user in all_users:
                                    user['profilePhoto'] = get_my_blob_name(user.get('profileBlobId'))
                            case 'fullname':
                                for user in all_users:
                                    user['fullname'] = f'{user.get("firstname")} {user.get("lastname")}'
                            case 'withRoles':
                                for user in all_users:
                                    user['roles'] = get_users_roles(user.get('userId'))[user.get('userId')]
                            case '_':
                                pass  # for now, no default use case

            response = make_response(jsonify({
                'success': True,
                'result': all_users,
                'message': None
            }), 200)
            return response
        else:
            return make_response(jsonify({
                'success': False,
                'result': 'user/no-users',
                'message': 'Keine User gefunden!'
            }))
    return make_response(jsonify({
        'success': False,
        'result': 'auth/no-session',
        'message': 'Keine Sitzung gefunden'
    }))


def get_mydata_route_v():
    session_id = request.cookies.get('tio_session_id')
    frontend_data = request.get_json() if request.method == 'POST' else {}
    if session_id:
        user_session = UserSession.KeywordQuery(session_id=session_id.encode())[0]
        if user_session:
            user = User.GetUserByID(user_session.user_id)

            return make_response(jsonify({
                'success': True,
                'result':
                    {
                        'name': [user.firstname, user.lastname],
                        'user_data': {
                            'userId': user.user_id,
                            'firstname': user.firstname,
                            'lastname': user.lastname,
                            'email': user.email,
                            'phone': user.phone,
                            'gender': user.gender,
                            'title': user.title,
                            'function': user.function,
                            'profilePhoto': get_my_blob_name(user.profile_blob_id),
                            'profileBlobId': user.profile_blob_id
                        }
                    },
                'error': None
            }), 200)
    else:
        # todo hier statt 200, 401 returnen und im frontend entsprechend reagieren
        return make_response(jsonify({
            'success': False,
            'result': 'auth/not-authorized',
            'error': "No session found"
        }), 200)


def update_mydata_route_v():
    session_id = request.cookies.get('tio_session_id')
    frontend_data = request.get_json() if request.method == 'POST' else {}

    if session_id:
        user_session = UserSession.KeywordQuery(session_id=session_id.encode())[0]
        if user_session:
            if not frontend_data:
                return make_response(jsonify({
                    'success': False,
                    'result': 'user/no-data',
                    'error': "No data found."
                }), 200)

            user = User.GetUserByID(user_session.user_id)

            success, result, error = update_user(user, frontend_data)

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


def update_user_route_v():
    # todo: diese methode und update_mydata_route_v zu einer vereinen
    session_id = request.cookies.get('tio_session_id')
    frontend_data = request.get_json() if request.method == 'POST' else {}

    if session_id:
        user_session = UserSession.KeywordQuery(session_id=session_id.encode())[0]
        if user_session:
            if not frontend_data:
                return make_response(jsonify({
                    'success': False,
                    'result': 'user/no-data',
                    'error': "No data found."
                }), 200)

            user = User.KeywordQuery(user_id=frontend_data.get('userId'))

            success, result, error = update_user(user, frontend_data)

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


def user_first_login_route_v():
    session_id = request.cookies.get('tio_session_id')
    frontend_data = request.get_json() if request.method == 'POST' else {}
    if session_id:
        user_session = UserSession.KeywordQuery(session_id=session_id.encode())[0]

        if request.method == 'GET':
            user = get_user_object(user_session.user_id)
            if int(user.first_login):
                return make_response(jsonify({
                    'success': True,
                    'result': 'user/first-login',
                    'error': None
                }))
            else:
                return make_response(jsonify({
                    'success': False,
                    'result': 'user/not-first-login',
                    'error': None
                }))
        if request.method == 'POST':

            if user_session:
                if not frontend_data:
                    return make_response(jsonify({
                        'success': False,
                        'result': 'user/no-data',
                        'error': "No data found."
                    }), 200)

                old_password = frontend_data.get('oldPW')
                new_password = frontend_data.get('newPW')

                user = get_user_object(user_session.user_id)

                if check_login(user, old_password):
                    success, result, error = update_user_pw(user, new_password)
                    if success:
                        remove_first_login_flag(user)
                    return make_response(jsonify({
                        'success': success,
                        'result': result,
                        'error': error
                    }))
                else:
                    return make_response(jsonify({
                        'success': False,
                        'result': 'auth/old-pw-wrong',
                        'error': "Das alte Passwort ist nicht korrekt."
                    }))


# todo: move to userpw
def user_change_password_route_v():
    session_id = request.cookies.get('tio_session_id')
    frontend_data = request.get_json() if request.method == 'POST' else {}
    if session_id:
        user_session = UserSession.KeywordQuery(session_id=session_id.encode())[0]

        if user_session:
            if not frontend_data:
                return make_response(jsonify({
                    'success': False,
                    'result': 'user/no-data',
                    'error': "No data found."
                }), 200)

            old_password = frontend_data.get('oldPW')
            new_password = frontend_data.get('newPW')

            user = get_user_object(user_session.user_id)

            if check_login(user, old_password):
                success, result, error = update_user_pw(user, new_password)

                return make_response(jsonify({
                    'success': success,
                    'result': result,
                    'error': error
                }))
            else:
                return make_response(jsonify({
                    'success': False,
                    'result': 'auth/old-pw-wrong',
                    'error': "Das alte Passwort ist nicht korrekt."
                }))


# todo: move to userpw
def update_user_password_route_v():
    session_id = request.cookies.get('tio_session_id')
    frontend_data = request.get_json() if request.method == 'POST' else {}
    if session_id:
        user_session = UserSession.KeywordQuery(session_id=session_id.encode())[0]

        if user_session:
            if not frontend_data:
                return make_response(jsonify({
                    'success': False,
                    'result': 'user/no-data',
                    'error': "No data found."
                }), 200)

            user_id = frontend_data.get('userId')
            new_password = frontend_data.get('password')
            user = get_user_object(user_id)

            success, result, error = update_user_pw(user, new_password)

            return make_response(jsonify({
                'success': success,
                'result': result,
                'error': error
            }))


def set_user_account_status_route_v():
    session_id = request.cookies.get('tio_session_id')
    frontend_data = request.get_json() if request.method == 'POST' else {}
    if session_id:
        user_session = UserSession.KeywordQuery(session_id=session_id.encode())[0]

        if user_session:
            if request.method == 'GET':
                user = User.GetUserByID(user_session.user_id)
                if user:
                    return make_response(jsonify({
                        'success': True,
                        'result': user.active,
                        'error': None
                    }))
                else:
                    return make_response(jsonify({
                        'success': False,
                        'result': 'user/no-user',
                        'error': "Der User konnte in der Datenbank nicht gefunden werden. Bitte an IT wenden."
                    }))
            else:
                if not frontend_data:
                    return make_response(jsonify({
                        'success': False,
                        'result': 'user/no-data',
                        'error': "Es wurden leider keine Daten übermittelt."
                    }), 200)

                user = User.KeywordQuery(user_id=frontend_data.get('userId'))
                success, result, error = change_user_account_status(user, int(frontend_data.get('accountStatus')))

                return make_response(jsonify({
                    'success': success,
                    'result': result,
                    'error': error
                }), 200)

