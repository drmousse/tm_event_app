#!/usr/bin/python3
# -*- coding: utf-8 -*-

# core imports
import sqlalchemy
from datetime import datetime
from flask import request, jsonify, make_response

# custom imports
from apiversion import api_version
from models import (
    EventFormat
)


# GLOBALS


# FUNCTIONS
def get_all_event_formats_route_v():
    response = make_response(jsonify({'tio_event_format': EventFormat.Query()}), 200)
    return response
