#!/usr/bin/python3
# -*- coding: utf-8

# core imports
import os

# custom imports


# GLOBALS
def get_api_key(key_provider):
    if not isinstance(key_provider, str):
        raise TypeError("<<Provider name is not a string>>")
    return os.environ.get(f'MCA_{key_provider.upper()}_API_KEY', None)

