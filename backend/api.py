#!/usr/bin/python3
# -*- coding: utf-8

# core imports
import os
from dotenv import load_dotenv

# custom imports


# KEYS
# loading env variables
load_dotenv()


TIO_API_APP_KEY = os.getenv('TIO_API_APP_KEY')
TIO_API_REFRESH_KEY = os.getenv('TIO_API_REFRESH_KEY')
TIO_API_ACCESS_KEY = os.getenv('TIO_API_ACCESS_KEY')

PW_STRING = f'{TIO_API_APP_KEY}-{{}}'
