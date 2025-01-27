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
    Games
)
from interfaces import (
    check_event_exist,
    create_event,
    update_blob_w_object_id,
    get_event,
    get_events,
    get_my_blob_name,
    get_event_format_name,
    get_role_access_events,
    get_upcoming_events,
    set_event_status
)


# GLOBALS


# FUNCTIONS
def create_event_route_v():
    session_id = request.cookies.get('tio_session_id')
    frontend_data = request.get_json() if request.method == 'POST' else {}

    if session_id:
        user_session = UserSession.KeywordQuery(session_id=session_id.encode())[0]

        if user_session:
            num_teams = frontend_data.get('numTeams')
            multi_mode = int(frontend_data.get('multiMode'))
            station_duplicates = None
            challenge_helper = None
            if multi_mode:
                station_duplicates = int(frontend_data.get('stationDuplicates'))
                challenge_helper = frontend_data.get('challengeHelper')
            new_event = {
                'customer': frontend_data.get('eventName'),
                'event_date': parse_date(frontend_data.get('eventDate')),
                'event_format': frontend_data.get('selectedEventFormat')['formatID'],
                'created_at': datetime.now(),
                'creator_id': user_session.user_id,
                'start_fcast': parse_date(frontend_data.get('eventStart')),
                'end_fcast': parse_date(frontend_data.get('eventEnd')),
                'event_blob_id': frontend_data.get('eventBlobId'),
                'greeting_duration': frontend_data.get('greetingDuration'),
                'challenges_duration': frontend_data.get('challengesDuration'),
                'transfer_duration': frontend_data.get('transferDuration'),
                'ceremony_duration': frontend_data.get('ceremonyDuration'),
                'multi_mode': frontend_data.get('multiMode'),
                'station_duplicates': frontend_data.get('stationDuplicates'),
                'event_lead_id': frontend_data.get('eventLeadId'),
                'status': 0,
                'status_type': 'event',
                'num_teams': num_teams
            }

            selected_games = frontend_data.get('selectedGames')
            blob_update = None

            if check_event_exist(new_event['customer'], new_event['event_format'], new_event['event_date']):
                return make_response(jsonify({
                    'success': False,
                    'result': 'user/already-exists',
                    'message': 'Event already exists with these parameters.'
                }), 200)

            new_event, error_code, error_msg = create_event(
                new_event, num_teams, selected_games, multi_mode, station_duplicates, challenge_helper
            )

            if not new_event:
                # todo: anhand der fehlercodes entsprechende protokollierung durchfuehren
                if error_code == 'db_error':
                    pass
                elif error_code == 'unknown_error':
                    pass
                return make_response(jsonify({'success': False, 'result': error_code, 'error': error_msg}), 200)

            if frontend_data.get('eventPictureBlobId'):
                blob_id = frontend_data.get('eventPictureBlobId')
                blob_upload_date = parse_date(frontend_data.get('eventPictureBlobUploadDate'))
                blob_update = update_blob_w_object_id(blob_id, new_event.event_id, blob_upload_date, 'media/event')

            return make_response(jsonify({
                'success': True,
                'result': new_event.event_id,
                'blob_update': blob_update
            }), 200)

        return make_response(jsonify({
            'success': False,
            'result': 'auth/no-session',
            'message': 'Keine Sitzung gefunden'
        }))


def get_event_route_v():
    session_id = request.cookies.get('tio_session_id')
    frontend_data = request.get_json() if request.method == 'POST' else {}

    if session_id:
        user_session = UserSession.KeywordQuery(session_id=session_id.encode())[0]

        if user_session:
            if not frontend_data.get('eventId'):
                return make_response(jsonify({
                    'success': False,
                    'result': 'event/no-data',
                    'error': "Es wurden leider keine Daten übermittelt."
                }), 200)

            event_id = frontend_data['eventId']
            success, result, message = get_event(event_id)

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


def get_events_route_v():
    session_id = request.cookies.get('tio_session_id')
    frontend_data = request.get_json() if request.method == 'POST' else {}

    if session_id:
        user_session = UserSession.KeywordQuery(session_id=session_id.encode())[0]

        if user_session:
            if not frontend_data.get('eventStatus'):
                return make_response(jsonify({
                    'success': False,
                    'result': 'event/no-status',
                    'error': "Es wurden leider keine Daten übermittelt."
                }), 200)

            user = User.GetUserByID(user_session.user_id)

            event_status = frontend_data['eventStatus']
            success, events, message = get_events(get_event_status_number(event_status))
            events_dict = events

            if success:
                role_access_result, user_role_events = get_role_access_events(events, user)
                if role_access_result:
                    events_dict = user_role_events
                else:
                    success = False
                    events_dict = None
                    message = 'No events for the user.'

            return make_response(jsonify({
                'success': success,
                'result': events_dict,
                'message': message
            }), 200)

    return make_response(jsonify({
        'success': False,
        'result': 'auth/no-session',
        'message': 'Keine Sitzung gefunden'
    }))


def get_upcoming_events_route_v():
    session_id = request.cookies.get('tio_session_id')

    if session_id:
        user_session = UserSession.KeywordQuery(session_id=session_id.encode())[0]

        if user_session:
            success, result, message = get_upcoming_events()

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


def set_event_status_route_v():
    session_id = request.cookies.get('tio_session_id')
    frontend_data = request.get_json() if request.method == 'POST' else {}

    if session_id:
        user_session = UserSession.KeywordQuery(session_id=session_id.encode())[0]

        if user_session:
            # todo: posts harmonisieren. es sollten alle daten in data gepackt werden und data wird dann ausgepackt
            if not frontend_data.get('data'):
                return make_response(jsonify({
                    'success': False,
                    'result': 'event/no-data',
                    'error': "Es wurden leider keine Daten übermittelt."
                }), 200)

            new_event_status = frontend_data['data']['eventStatus']
            event_id = frontend_data['data']['eventId']
            success, result, message = set_event_status(event_id, new_event_status)

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
