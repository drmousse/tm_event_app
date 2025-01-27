#!/usr/bin/python3
# -*- coding: utf-8 -*-

# core imports
import os
from datetime import datetime
from flask import request, jsonify, make_response

# custom imports
import tools
import tioglobals
from apiversion import api_version
from appinformation import app_information
from models import (
    TioDB,
    Blobstore,
    UserSession
)


# GLOBALS


# FUNCTIONS
def get_api_version_route_v():
    response = make_response(jsonify({'tio_api_version': api_version}))
    response.set_cookie('tio_api_version', api_version, samesite='Lax')
    return response


def upload_blob_route_v():
    if not request.files:
        return make_response(jsonify({
            'success': False, 'result': 'user/no-file-uploaded', 'message': 'No file uploaded'
        }), 200)

    file, media_kind = tools.get_media_type(request.files)

    # todo: bin mir nicht sicher, ob dieser fall ueberhaupt eintreten kann
    if file.filename == '':
        return make_response(jsonify({
            'success': False, 'result': 'user/no-file-selected', 'message': 'No file selected'
        }), 200)

    if file:
        dt = datetime.now()
        data = file.read()
        blob_id = tools.generate_id(tioglobals.TIO_BLOBSTORE)
        filename = f'{blob_id}.{file.filename.split(".")[-1]}'
        new_blob = Blobstore(
            blob_id=blob_id,
            name=filename,
            original_filename=file.filename,
            data=data,
            blob_upload_date=dt,
            kind=media_kind,
            blob_type='image'  # todo: as soon as more types are supported, this needs to be more general
        )

        TioDB.add_object(new_blob)
        # todo: fotos werden in der db gespeichert und nachher wird per pfad und andere parameter
        #   geprüft, ob foto im frontend existiert. falls nicht, wird es aus dem backend geholt
        file_path = os.path.join(
            TioDB.app.config['UPLOAD_FOLDER'],
            media_kind,
            filename
        )
        file.seek(0)
        file.save(file_path)
        return make_response(jsonify({
            'success': True,
            'result': {'blob_id': blob_id, 'blob_upload_date': dt, 'filename': filename},
            'error': None
        }), 200)


def get_app_information_route_v():
    session_id = request.cookies.get('tio_session_id')

    if session_id:
        user_session = UserSession.KeywordQuery(session_id=session_id.encode())[0]

        if user_session:
            try:
                app_data = app_information()

                return make_response(jsonify({
                    'success': True,
                    'result': app_data,
                    'message': None
                }), 200)
            except Exception as e:
                return make_response(jsonify({
                    'success': False,
                    'result': 'bedb/get_app_information',
                    'message': str(e)
                }))

        return make_response(jsonify({
            'success': False,
            'result': 'auth/no-session',
            'message': 'Keine Sitzung gefunden'
        }))
