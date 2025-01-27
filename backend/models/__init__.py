#!/usr/bin/python3
# -*- coding: utf-8
#
# todo: at the moment, all models implement their own methods for ByKeys and KeywordQuery. in some future implementation
#   one could check, if via inheritance there could be a more generic way to implement this


__all__ = [
    'TioDB',
    'Blobstore',
    'ChallengeHelper',
    'Counter',
    'CsrfToken',
    'Event',
    'EventFormat',
    'EventGameComment',
    'EventLead',
    'EventRoundGroupDistribution',
    'EventSchedule',
    'EventScore',
    'EventSession',
    'Games',
    'GameStation',
    'Group',
    'Message',
    'OLC',
    'Roles',
    'StationLead',
    'StationScore',
    'Team',
    'User',
    'UserPW',
    'UserRoles',
    'UserSession',
    'UserSettings'
]

from .base import TioDB as TioDB
from .blobstore import Blobstore as Blobstore
from .challengehelper import ChallengeHelper as ChallengeHelper
from .counter import Counter as Counter
from .csrftoken import CsrfToken
from .event import Event as Event
from .eventformat import EventFormat
from .eventgamecomment import EventGameComment as EventGameComment
from .eventlead import EventLead as EventLead
from .eventroundgroupdistribution import EventRoundGroupDistribution as EventRoundGroupDistribution
from .eventschedule import EventSchedule as EventSchedule
from .eventscore import EventScore as EventScore
from .eventsession import EventSession as EventSession
from .games import Games as Games
from .gamestation import GameStation as GameStation
from .group import Group as Group
from .message import Message as Message
from .olc import OLC as OLC
from .roles import Roles as Roles
from .stationlead import StationLead as StationLead
from .stationscore import StationScore as StationScore
from .team import Team as Team
from .user import User as User
from .userpw import UserPW as UserPW
from .userroles import UserRoles as UserRoles
from .usersession import UserSession as UserSession
from .usersettings import UserSettings
