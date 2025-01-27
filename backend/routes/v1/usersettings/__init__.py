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
    UserSession,
    Games,
    UserSettings,
    EventFormat
)

# GLOBALS


# FUNCTIONS
def user_settings_route_v():
    """
        there are two modes: 'set' and 'get'. if it is 'get', we return all usersettings of
        that user. if it is 'set', we check data for key and value and set it to database.
        if the key does not exist, we create it.
    """
    frontend_data = request.get_json() if request.method == 'POST' else {}
    session_id = request.cookies.get('tio_session_id')

    if not session_id:
        return make_response(jsonify({'success': False, 'result': 'auth/no-res'}), 200)

    user_session = UserSession.KeywordQuery(session_id=session_id.encode())[0]
    user_settings = UserSettings.KeywordQuery(user_id=user_session.user_id)
    user_id = user_session.user_id

    request_mode = frontend_data.get('mode')

    if request_mode == 'get':
        print("bin in get")
        return make_response(jsonify({'success': True, 'tio_user_settings': user_settings}), 200)
    elif request_mode == 'set':
        print("bin in set")
        attrs = frontend_data.get('data')
        errors = []
        for attr in attrs:
            try:
                u_setting = UserSettings.ByKeys(attr['key'], user_id)
                if u_setting:
                    u_setting.value = attr['value']
                    u_setting.commit()
                else:
                    u_setting = UserSettings(setting_id=attr['key'], user_id=user_id, value=attr['value'])
                    TioDB.add_object(u_setting)
            except sqlalchemy.exc.IntegrityError as err:
                errors.append(f"user_setting_route_v, setting_id: {attr['key']}, value: {attr['value']}, err: {str(err)}")

        if errors:
            success = False
            result = 'db_error'
        else:
            success = True
            result = 'no_error'

        return make_response(jsonify({'success': success, 'result': result, 'error': errors}), 200)
