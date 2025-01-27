#!/usr/bin/python3
# -*- coding: utf-8 -*-


# imports
import os
import json
import bcrypt
import sqlalchemy
from datetime import datetime
from collections import defaultdict


# custom imports
import tools
import tioglobals
from eventschedulecreator import (
    create_event_schedule,
    generate_group_schedule,
    generate_tournament_schedule,
    event_schedule_creation_possible
)
from api import (
    TIO_API_APP_KEY,
    TIO_API_REFRESH_KEY,
    TIO_API_ACCESS_KEY,
    PW_STRING
)
from models import (
    TioDB,
    User,
    UserPW,
    UserSession,
    Games,
    GameStation,
    Group,
    StationLead,
    StationScore,
    Team,
    UserRoles,
    Event,
    EventFormat,
    EventScore,
    Blobstore,
    Roles,
    OLC,
    Message,
    EventGameComment,
    EventRoundGroupDistribution,
    ChallengeHelper
)
from pyasn1_modules.rfc4210 import Challenge


################################
# GENERAL FUNCTIONS
################################


################################
# BLOBSTORE
################################
def update_blob_w_object_id(blob_id, object_id, dt, blob_type):
    """

    :param blob_id: str
    :param object_id: str
    :param dt: datetime
    :param blob_type: str
    :return: bool
    """
    if isinstance(dt, str):
        dt = tools.parse_date(dt)

    blob = Blobstore.ByKeys(blob_id)
    if blob:
        blob.blob_type = blob_type
        blob.object_id = object_id
        blob.blob_upload_date = dt
        blob.commit()
        return True

    return False


def get_my_blob_name(blob_id):
    # todo: um valid erweitern
    try:
        blob = Blobstore.ByKeys(blob_id)
        return blob.name
    except Exception as e:
        return ''


################################
# CHALLENGEHELPER
################################
def create_challenge_helper(event_id, challenge_helper):
    ch_objs = []
    for ch in challenge_helper:
        if ch.get('gameId'):
            ch_objs.append(ChallengeHelper(event_id=event_id, game_id=ch['gameId'], user_id=ch['userId']))

    return ch_objs


################################
# EVENT
################################
def check_event_exist(customer, event_format, event_date):
    """
    Check if event exists. But not checking if there is more than one event.
    Be design. It should not be possible to have more than one event with same params.

    :param customer: str
    :param event_date: datetime
    :param event_format: str
    :return: bool
    """
    event = Event.KeywordQuery(customer=customer, event_date=event_date, event_format=event_format)
    return len(event) != 0


def create_event(event_params, num_teams, selected_games, multi_mode, station_duplicates, challenge_helper):
    new_event = Event(event_id=tools.generate_id(tioglobals.TIO_EVENT), **event_params)

    if not multi_mode:
        if not event_schedule_creation_possible(num_teams, len(selected_games)):
            return (False,
                    'event/creation-success-not-possible',
                    'Die ausgewählte Kombination Anzahl Challenges und Anzahl Teams ist nicht zulässig')

    teams = [Team(team_id=tools.generate_id(tioglobals.TIO_TEAM), number=i) for i in range(1, num_teams+1)]
    games = [g['gameID'] for g in selected_games]
    games_dict = {}
    groups = []
    team_group_distribution = defaultdict(list)
    game_stations = []
    station_scores = []
    station_helper = []
    event_scores = [EventScore(event_id=new_event.event_id, team_id=team.team_id) for team in teams]
    event_round_group_distributions = []

    for g in selected_games:
        games_dict[g['gameID']] = g

    num_groups = len(games_dict)

    group_names = [chr(65 + i) for i in range(num_groups)]

    for idx, team in enumerate(teams):
        idx_group_names = idx % num_groups
        groups.append(Group(event_id=new_event.event_id, team_id=team.team_id, name=group_names[idx_group_names]))
        team_group_distribution[group_names[idx_group_names]].append(team.team_id)

    if multi_mode:
        group_schedule = generate_group_schedule(num_groups)

        for round_number in range(1, len(games)+1):
            for position, game_id in enumerate(games):
                event_round_group_distributions.append(
                    EventRoundGroupDistribution(event_id=new_event.event_id,
                                                game_id=game_id,
                                                group_name=group_schedule[round_number-1][position],
                                                round_number=round_number,
                                                position=position)
                )

        new_event.group_distribution = json.dumps(group_schedule)
        for group_name, teams_ids in team_group_distribution.items():
            group_schedule = generate_tournament_schedule(teams_ids, station_duplicates, num_groups)

            _game_stations, _stations_scores = create_game_stations_multiple(
                new_event.event_id, group_name, group_schedule, games, games_dict
            )
            game_stations += _game_stations
            station_scores += _stations_scores

        station_helper = create_challenge_helper(new_event.event_id, challenge_helper)

    else:
        event_schedule = create_event_schedule(teams, games)
        game_stations, station_scores = create_game_stations(new_event.event_id, event_schedule, games_dict)

    try:
        TioDB.add_objects(
            [new_event] +
            game_stations +
            station_scores +
            teams +
            groups +
            event_scores +
            event_round_group_distributions +
            station_helper
        )
    except sqlalchemy.exc.IntegrityError as err:
        return False, 'db_error', str(err)
    except Exception as err:
        return False, 'unknown_error', str(err)

    return new_event, 'event/creation-success', None


def get_event(event_id):
    event = Event.ByKeys(event_id=event_id)

    if not event:
        return False, 'event/not_found', 'Es gibt kein Event mit dieser ID.'

    multi_mode = int(event.multi_mode)

    event_lead = User.GetUserByID(event.event_lead_id)
    game_stations = GameStation.KeywordQuery(event_id=event_id)
    station_scores = []
    game_station_ids = set()
    station_leads_ids = set()
    station_leads = []
    game_ids = set()
    games = {}
    team_ids = set()
    teams = {}
    station_lead_distribution = []
    teams_list = []
    team_placements = {}
    game_names = {}
    game_comments = {}
    event_scores = {}
    groups_round_distribution = defaultdict(list)
    groups = None
    group_distribution = defaultdict(list)

    if multi_mode:
        groups_round_distribution_objects = EventRoundGroupDistribution.KeywordQuery(event_id=event_id)

        for grdo in groups_round_distribution_objects:
            groups_round_distribution[grdo.game_id].append(grdo.convert_to_dict())

        for position_content in groups_round_distribution.values():
            position_content.sort(key=lambda x: x['round_number'])

        groups = Group.KeywordQuery(event_id=event.event_id)
        for group in groups:
            group_distribution[group.name].append(group.team_id)
    else:
        groups_round_distribution = None
        group_distribution = None

    if groups:
        groups_dict = [g.convert_to_dict() for g in groups]
    else:
        groups_dict = None

    event_dict = event.convert_to_dict()
    if event_dict.get('event_blob_id'):
        event_dict['event_blob_name'] = get_my_blob_name(event.event_blob_id)

    for g in game_stations:
        station_leads_ids.add(g.station_lead_id)
        game_station_ids.add(g.game_station_id)

    for gs_id in game_station_ids:
        station_scores += StationScore.KeywordQuery(event_id=event_id, game_station_id=gs_id)

    for g in game_stations:
        game_ids.add(g.game_id)

    for sl_id in station_leads_ids:
        station_leads.append(User.GetUserByID(sl_id))

    # number of games has to be equal to number of groups
    counter = 0
    for g_id in game_ids:
        game = Games.KeywordQuery(game_id=g_id)[0]
        games[g_id] = game
        _, team_placements[g_id], _ = get_station_team_placements(event, game)
        game_names[g_id] = game.name

    # getting game comments
    for g_id in game_ids:
        egc_success, egc, _ = get_event_game_comment(event_id, g_id)
        if egc_success:
            game_comments[g_id] = egc.comment
        else:
            game_comments[g_id] = ''

    for gs in game_stations:
        team_ids.add(gs.team_a_id)
        team_ids.add(gs.team_b_id)

    for t_id in team_ids:
        team = Team.ByKeys(team_id=t_id).convert_to_dict()
        es = EventScore.ByKeys(event_id=event_id, team_id=t_id)
        teams[t_id] = team
        teams_list.append(team)
        event_scores[t_id] = es.additional_points if es else None

    for g_id, g in games.items():
        for gs in game_stations:
            if gs.game_id == g_id:
                station_lead_distribution.append({
                    'game_name': g.name,
                    'lead_id': gs.station_lead_id,
                    'game_id': g_id
                })
                break

    final_placements = get_event_scores(event_id)

    if final_placements:
        for idx, fp in enumerate(final_placements):
            score = fp['score'] if fp['score'] else 0
            add_points = fp['additional_points'] if fp['additional_points'] else 0
            total = score + add_points if score + add_points > 0 else ''
            fp['placement'] = idx + 1
            fp['score_points'] = total
            fp['team_name'] = teams[fp['team_id']]['name']
            fp['team_number'] = teams[fp['team_id']]['number']

    if not (event or game_stations or station_leads):
        return False, 'bedb/get_event', 'Es wurden nicht alle Daten gefunden. Bitte an IT wenden.'

    return True, {
        'event': event_dict,
        'event_lead': f'{event_lead.firstname} {event_lead.lastname}',
        'game_stations': [gs.convert_to_dict() for gs in game_stations],
        'station_leads': [sl.convert_to_dict() for sl in station_leads],
        'games': [{g_id:g_object.convert_to_dict()} for g_id, g_object in games.items()],
        'teams': teams,
        'stations_scores': [s.convert_to_dict() for s in station_scores],
        'station_lead_distribution': station_lead_distribution,
        'teams_list': teams_list,
        'event_states': [o.convert_to_dict() for o in OLC.KeywordQuery(type='event')],
        'team_placements': team_placements,
        'game_names': game_names,
        'final_placements': final_placements,
        'game_comments': game_comments,
        'event_scores': event_scores,
        'groups_round_distribution': groups_round_distribution,
        'group_distribution': group_distribution,
        'groups': groups_dict
    }, None


def get_events(status):
    if status is None:
        return False, 'event/not-correct-status', 'Leider konnte dieser Eventstatus nicht gefunden werden.'

    events = Event.KeywordQuery(status=status)

    if events:
        return True, events, None

    return False, 'event/no-events-found', 'Zu diesem Status existieren noch keine Events.'


def get_role_access_events(events, user):
    def append_event(view, ev):
        view.append(ev.convert_to_dict())
        view[-1]['blob_file_name'] = get_my_blob_name(ev.event_blob_id)
        view[-1]['event_format_name'] = get_event_format_name(ev.event_format)

    user_roles = get_user_roles(user.user_id)
    if user_roles is None:
        return False, None

    mix_view = []
    manage_view = []
    user_view = []
    result = False

    user_role_names = [r['name'] for r in user_roles]

    for event in events:
        station_lead_ids = get_game_station_lead_ids(event.event_id)

        is_event_lead = event.event_lead_id == user.user_id
        is_creator = event.creator_id == user.user_id
        is_station_lead = user.user_id in station_lead_ids
        is_admin = tioglobals.TIO_CROLE_ADMIN in user_role_names
        is_manager = tioglobals.TIO_CROLE_MANAGER in user_role_names

        if is_station_lead:
            if is_event_lead or is_creator or is_manager or is_admin:
                append_event(mix_view, event)
            else:
                append_event(user_view, event)
        elif is_event_lead or is_creator or is_admin or is_manager:
            append_event(manage_view, event)
        else:
            challenge_helper_games = ChallengeHelper.KeywordQuery(event_id=event.event_id, user_id=user.user_id)
            for chg in challenge_helper_games:
                if chg.game_id:
                    # it's enough to find on game, where the user is helper
                    append_event(user_view, event)

    if mix_view or manage_view or user_view:
        result = True

    user_role_events = {
        'mix': mix_view,
        'manage': manage_view,
        'user': user_view
    }

    return result, user_role_events


def get_upcoming_events():
    success_active_events, active_events, message_active_events = get_events(50)
    success_upcoming_events, upcoming_events, message_upcoming_events = get_events(0)

    if not (success_active_events or success_upcoming_events):
        # if there are no active and no upcoming events, then we can take the result
        # of either one of both. the same for mesage
        return False, None, 'Es gibt weder aktive, noch geplante Events.'

    if success_active_events:
        active_events_dict = [e.convert_to_dict() for e in active_events]
        for event in active_events_dict:
            event['event_blob_name'] = get_my_blob_name(event['event_blob_id'])
            event['event_format_name'] = get_event_format_name(event['event_format'])
    else:
        active_events_dict = None

    if success_upcoming_events:
        today = datetime.now().date()
        upcoming_events_dict = []
        for e in upcoming_events:
            if e.event_date >= today:
                upcoming_events_dict.append(e.convert_to_dict())

            for event in upcoming_events_dict:
                event['event_blob_name'] = get_my_blob_name(event['event_blob_id'])
                event['event_format_name'] = get_event_format_name(event['event_format'])

        if upcoming_events_dict:
            upcoming_events_dict.sort(key=lambda x: x['event_date'])
        else:
            upcoming_events_dict = None
    else:
        upcoming_events_dict = None

    return True, {'activeEvents': active_events_dict, 'upcomingEvents': upcoming_events_dict}, None


def set_event_status(event_id, new_status):
    event = Event.ByKeys(event_id=event_id)

    if new_status == 50:
        try:
            event.status = new_status
            event.start_actual = datetime.now()
            event.commit()
            return True, None, None
        except Exception as e:
            return False, 'bedb/set_event_status::50', str(e)

    elif new_status == 100:
        try:
            event.status = new_status
            event.end_actual = datetime.now()
            event.commit()
            return True, None, None
        except Exception as e:
            return False, 'bedb/set_event_status::100', str(e)

    elif new_status == 180:
        try:
            event.status = new_status
            event.commit()
            return True, None, None
        except Exception as e:
            return False, 'bedb/set_event_status::180', str(e)

    elif new_status == 0:
        try:
            event.status = new_status
            event.commit()
            return True, None, None
        except Exception as e:
            return False, 'bedb/set_event_status::0', str(e)

    return False, 'bedb/set_event_status::no-correct-status', ('Es wurde ein unbekannter Eventstatus übermittelt. '
                                                               'Bitte IT kontaktieren.')


################################
# EVENTFORMAT
################################
def get_event_formats():
    return EventFormat.Query()


def get_event_format(format_id):
    return EventFormat.ByKeys(format_id=format_id)


def get_event_format_name(format_id):
    ef = EventFormat.ByKeys(format_id=format_id)
    if ef:
        return ef.name

    return None


# EVENTLEAD


################################
# EVENTSCORE
################################
def get_event_scores(event_id):
    event_scores = EventScore.KeywordQuery(event_id=event_id)

    def get_total_points(es):
        if not es.score:
            return 0

        if not es.additional_points:
            return es.score

        return int(es.score) + int(es.additional_points)

    if event_scores:
        event_scores.sort(key=get_total_points, reverse=True)
        event_scores_dict = [es.convert_to_dict() for es in event_scores]

        return event_scores_dict

    return None


def update_event_score_by_gamestation(event_id):
    """
    Updates event scores of all teams by gathering game station information
    """
    event = Event.ByKeys(event_id=event_id)
    game_stations = GameStation.KeywordQuery(event_id=event_id)
    game_ids = set()
    team_placements = {}
    final_placements = defaultdict(lambda: defaultdict(int))

    for g in game_stations:
        game_ids.add(g.game_id)

    for g_id in game_ids:
        game = Games.KeywordQuery(game_id=g_id)[0]
        _, team_placements[g_id], _ = get_station_team_placements(event, game)

    for team_placement in team_placements.values():
        for team in team_placement:
            team_id = team['team_id']
            score_points = team['score_points']
            final_placements[team_id]['score_points'] += score_points

    sorted_final_placements = sorted(
        [{'team_id': team_id, 'score_points': scores['score_points']}
         for team_id, scores in final_placements.items()],
        key=lambda x: x['score_points'],
        reverse=True
    )

    new_event_scores = []
    for tp in sorted_final_placements:
        es = EventScore.ByKeys(event_id=event_id, team_id=tp['team_id'])
        if es:
            es.score = tp['score_points']
        else:
            new_es = EventScore(event_id=event_id, team_id=tp['team_id'], score=tp['score_points'])
            new_event_scores.append(new_es)

    TioDB.commit()

    if new_event_scores:
        TioDB.add_objects(new_event_scores)

    # todo: error handling fehlt

    return True, None, None


def update_event_score(event_id, team_id, score):
    try:
        es = EventScore.ByKeys(event_id=event_id, team_id=team_id)
        if es:
            es.score = score
            es.commit()
        else:
            es = EventScore(event_id=event_id, team_id=team_id, score=score)
            TioDB.add_object(es)
        return True, None, None

    except Exception as e:
        return False, 'bedb/update_event_score', str(e)


def update_event_scores(event_id, event_scores):
    # todo: function will stop, when only one object fails
    #   we need to change it, so that it keeps moving and collects all errors and then
    #   returns an error
    try:
        for team_id, add_score in event_scores.items():
            es = EventScore.ByKeys(event_id=event_id, team_id=team_id)
            if es:
                es.additional_points = add_score
                es.commit()
            else:
                es = EventScore(event_id=event_id, team_id=team_id, additional_points=add_score)
                TioDB.add_object(es)

        return True, None, None

    except Exception as e:
        return False, 'bedb/update_event_scores', str(e)


# EVENTSESSION


################################
# EVENTGAMECOMMENT
################################
def get_event_game_comment(event_id, game_id):
    egc = EventGameComment.ByKeys(event_id=event_id, game_id=game_id)
    if egc:
        return True, egc, None

    return False, None, 'Kein Challengekommentar gefunden.'


def set_event_game_comment(event_id, game_id, comment):
    try:
        egc = EventGameComment.ByKeys(event_id=event_id, game_id=game_id)
        if egc:
            egc.comment = comment
            egc.commit()
        else:
            egc = EventGameComment(event_id=event_id, game_id=game_id, comment=comment)
            TioDB.add_object(egc)

        return True, None, None
    except Exception as e:
        return False, 'bedb/set_event_game_comment', str(e)


################################
# GAMES
################################
def create_game(game_params):
    if Games.ByKeys(game_params['name']):
        return (
            False,
            'game/already-exists',
            'Challenge existiert bereits. Wähle bitte einen anderen Namen für die Challenge.'
        )

    new_game = Games(game_id=tools.generate_id(tioglobals.TIO_GAMES), **game_params)

    try:
        TioDB.add_object(new_game)
    except sqlalchemy.exc.IntegrityError as err:
        return False, 'db_error', str(err)
    except Exception as err:
        return False, 'unknown_error', str(err)

    return new_game, None, None


def get_all_games():
    try:
        games = Games.Query()
        return True, games, None
    except Exception as err:
        return False, 'bedb/get_all_games', str(err)


def change_game_status(game, active):
    # todo: methode umbenennen, da status keinen sinn ergibt
    try:
        game.active = active
        game.commit()
        return True, 'game/status_change-success', None
    except sqlalchemy.exc.IntegrityError as err:
        return False, 'game/status_change-failed', str(err)


def update_game(game, data):
    if game:
        # todo: checken, ob essentielle daten wie vorname, etc. geändert werden dürfen
        # todo: robuster gestalten. bspw. mit .get
        game.name = data['name']
        game.duration = data['duration']
        game.score_type = data['scoreType']
        game.score_counting = data['scoreCounting']
        game.description = data['description']

        if data.get('gameBlobId'):
            game.game_blob_id = data['gameBlobId']

        blob_id = data.get('gameBlobId')
        if blob_id:
            game.game_blob_id = blob_id
            blob = Blobstore.ByKeys(blob_id)
            blob.object_id = game.game_id

        try:
            TioDB.commit()
        except sqlalchemy.exc.IntegrityError as err:
            return False, 'db_error', str(err)

        return True, 'game/update-success', None

    return False, 'game/game-not-found', 'Kritisch: Challenge wurde nicht gefunden. Bitte an IT wenden.'


################################
# GAMESTATION
################################
def create_game_stations(event_id, event_schedule, games):
    game_stations = []
    station_scores = []

    for game_id, parties in event_schedule.items():
        for game_no, party in enumerate(parties, start=1):
            if not party:
                continue
            game_station_id = tools.generate_id(tioglobals.TIO_GAMESTATION)
            game_stations.append(GameStation(
                game_station_id=game_station_id,
                event_id=event_id,
                game_id=game_id,
                game_no=game_no,
                team_a_id=party[0],
                team_b_id=party[1],
                status=0,
                status_type='game',
                station_lead_id=games[game_id]['gameLeadId'],
                num_rounds=games[game_id]['numRounds'],
            ))

            for i in range(1, int(games[game_id]['numRounds']) + 1):
                station_scores.append(StationScore(
                    event_id=event_id,
                    game_station_id=game_station_id,
                    team_id=party[0],
                    round_number=i
                ))
                station_scores.append(StationScore(
                    event_id=event_id,
                    game_station_id=game_station_id,
                    team_id=party[1],
                    round_number=i
                ))

    return game_stations, station_scores


def create_game_stations_multiple(event_id, group_name, team_distributions, game_ids, games):
    game_stations = []
    station_scores = []

    for idx, td in enumerate(team_distributions):
        game_id = game_ids[idx]
        game_dict = games[game_id]
        for party in td:
            game_station_id = tools.generate_id(tioglobals.TIO_GAMESTATION)
            game_stations.append(GameStation(
                game_station_id=game_station_id,
                event_id=event_id,
                game_id=game_id,
                game_no=idx,
                team_a_id=party[0],
                team_b_id=party[1],
                status=0,
                status_type='game',
                station_lead_id=game_dict['gameLeadId'],
                num_rounds=game_dict['numRounds'],
                group_name=group_name
            ))

            for i in range(1, int(game_dict['numRounds']) + 1):
                station_scores.append(StationScore(
                    event_id=event_id,
                    game_station_id=game_station_id,
                    team_id=party[0],
                    round_number=i
                ))
                station_scores.append(StationScore(
                    event_id=event_id,
                    game_station_id=game_station_id,
                    team_id=party[1],
                    round_number=i
                ))

    return game_stations, station_scores


def get_game_station_lead_ids(event_id):
    return GameStation.GetStationLeadIDs(event_id=event_id)


def get_game_stations(event_id, user_id):
    event = Event.ByKeys(event_id=event_id)
    # we have to check, if we have a station lead or a helper
    # if this function is called, that means, that the user was
    # able to click on link to get here. therefore, we can assume
    # that the user has a valid entry in db which shows him/her as
    # a helper
    game_stations = GameStation.KeywordQuery(event_id=event_id, station_lead_id=user_id)
    if game_stations:
        game = Games.KeywordQuery(game_id=game_stations[0].game_id)[0]
    else:
        # the assumption is that a helper can only help out at one station
        ch = ChallengeHelper.KeywordQuery(event_id=event_id, user_id=user_id)[0]
        game = Games.KeywordQuery(game_id=ch.game_id)[0]
        # and furthermore, since for all gamestations the game id is
        # identical, we now get our game stations via challenge helper game id
        game_stations = GameStation.KeywordQuery(event_id=event_id, game_id=game.game_id)
    team_ids = set()
    teams = {}
    teams_list = []
    teams_scores = {}
    groups_round_distribution = defaultdict(list)
    groups = None
    group_distribution = defaultdict(list)

    if int(event.multi_mode):
        groups_round_distribution_objects = EventRoundGroupDistribution.KeywordQuery(event_id=event_id)

        for grdo in groups_round_distribution_objects:
            groups_round_distribution[grdo.game_id].append(grdo.convert_to_dict())

        for position_content in groups_round_distribution.values():
            position_content.sort(key=lambda x: x['round_number'])

        groups = Group.KeywordQuery(event_id=event.event_id)
        for group in groups:
            group_distribution[group.name].append(group.team_id)
    else:
        groups_round_distribution = None
        group_distribution = None

    if groups:
        groups_dict = [g.convert_to_dict() for g in groups]
    else:
        groups_dict = None

    game_comment_success, game_comment, _ = get_event_game_comment(event_id, game.game_id)
    if game_comment_success:
        game_comment = game_comment.comment
    else:
        game_comment = ''

    event_dict = event.convert_to_dict()
    if event_dict.get('event_blob_id'):
        event_dict['event_blob_name'] = get_my_blob_name(event.event_blob_id)

    for gs in game_stations:
        team_ids.add(gs.team_a_id)
        team_ids.add(gs.team_b_id)

    for t_id in team_ids:
        team = Team.ByKeys(team_id=t_id).convert_to_dict()
        teams[t_id] = team
        teams_list.append(team)

    gs_stations = [gs.convert_to_dict() for gs in game_stations]
    for gs_station in gs_stations:
        gs_station['name'] = game.name

    if event.multi_mode:
        # for multi mode all game numbers within the same station should be equal
        game_no = game_stations[0].game_no
    else:
        game_no = None

    for gs in game_stations:
        for i in range(1, gs.num_rounds+1):
            if gs.game_station_id not in teams_scores:
                teams_scores[gs.game_station_id] = {}

            if gs.team_a_id in teams_scores[gs.game_station_id]:
                teams_scores[gs.game_station_id][gs.team_a_id][i] = ''
            else:
                teams_scores[gs.game_station_id][gs.team_a_id] = {i: ''}

            if gs.team_b_id in teams_scores[gs.game_station_id]:
                teams_scores[gs.game_station_id][gs.team_b_id][i] = ''
            else:
                teams_scores[gs.game_station_id][gs.team_b_id] = {i: ''}

    for gs_id in teams_scores:
        for team_id in teams_scores[gs_id]:
            for round_number in teams_scores[gs_id][team_id]:
                st_score = StationScore.ByKeys(event_id, gs_id, team_id, round_number)
                if st_score:
                    teams_scores[gs_id][team_id][round_number] = st_score.score

    _, team_placement, _ = get_station_team_placements(event, game)

    res = {
        'event': event_dict,
        'game_stations': gs_stations,
        'game': game.convert_to_dict(),
        'teams': teams,
        'teams_list': teams_list,
        'game_blob_name': get_my_blob_name(game.game_id),
        'team_placement': team_placement,
        'team_scores': teams_scores,
        'game_no': game_no,
        'game_comment': game_comment,
        'groups_rounds_distribution': groups_round_distribution,
        'groups': groups_dict,
        'group_distribution': group_distribution
    }
    return True, res, None


################################
# Message
################################
def create_message(user_id, user_name, message_type, content, **kwargs):
    parent_id = kwargs.get('parent_id')
    if parent_id:
        sub_messages = Message.KeywordQuery(parent_message_id=parent_id)
        len_sub_messages = len(sub_messages)
        if len_sub_messages == 0:
            highest_num = 0
        elif len_sub_messages == 1:
            highest_num = sub_messages[0].message_number
        else:
            highest_num = sub_messages[0].message_number
            for msg_index in range(1, len_sub_messages):
                if sub_messages[msg_index].message_number > highest_num:
                    highest_num = sub_messages[msg_index].message_number

        # after this, the highest number should now be set
        highest_num += 1

    message = Message(
        message_id=tools.generate_id(tioglobals.TIO_MESSAGE),
        user_id=user_id,
        user_name=user_name,
        message_type=message_type,
        content=content,
        created_on=datetime.now()
    )

    if parent_id:
        message.parent_message_id = parent_id
        message.message_number = highest_num

    try:
        TioDB.add_object(message)

        message = message.convert_to_dict()

        # we are always assuming, that the creator of the message is the user itself and therefore the message
        # is editable for the user
        message['is_editable'] = True

        return True, {'message': message, 'parent_id': parent_id}, None
    except Exception as e:
        return False, 'bedb/create_message', str(e)


def get_messages(message_type):
    messages = Message.KeywordQuery(message_type=message_type)
    if messages:
        return True, messages, None

    return False, None, 'Keine Nachrichten gefunden.'


def get_messages_sorted_by(message_type, sorted_by, reverse=False):
    messages = Message.KeywordQuery(message_type=message_type)
    if messages:
        sub_messages = defaultdict(list)
        parent_messages = []
        for message in messages:
            if message.parent_message_id:
                sub_messages[message.parent_message_id].append(message)
            else:
                parent_messages.append(message)

        sorted_parent_messages = sorted(parent_messages, key=lambda x: getattr(x, sorted_by), reverse=reverse)
        sorted_parent_messages = [e.convert_to_dict() for e in sorted_parent_messages]

        if len(sub_messages):
            for parent_id, message in sub_messages.items():
                sub_messages[parent_id] = sorted(sub_messages[parent_id],
                                                 key=lambda x: getattr(x, sorted_by), reverse=False)

            for parent_id, message in sub_messages.items():
                sub_messages[parent_id] = [e.convert_to_dict() for e in sub_messages[parent_id]]
        else:
            sub_messages = []

        return True, {'parent_messages': sorted_parent_messages, 'sub_messages': sub_messages}, None

    return False, None, 'Keine Nachrichten gefunden.'


def update_message(message_id, content):
    message = Message.ByKeys(message_id=message_id)
    message.content = content
    message.edited_on = datetime.now()
    message.commit()

    return True, None, None


def delete_message(message_id):
    # check if there are submessages. if so, message can't be deleted
    pass


def handle_message(user, message_data):
    if message_data['editType'] == tioglobals.TIO_MESSAGE_EDIT:
        return update_message(message_data['messageId'], message_data['content'])

    if message_data['editType'] == tioglobals.TIO_MESSAGE_REPLY:
        return create_message(
            user.user_id,
            user.get_full_name(),
            tioglobals.TIO_MESSAGE_GENERAL,
            message_data['content'],
            **{'parent_id': message_data['messageId']}
        )

    return False, 'bedb/handle_message', 'Unbekannter Editiermodus.'


# OLC


################################
# ROLES
################################
def get_roles(role_type):
    try:
        roles = Roles.KeywordQuery(type=role_type)
        roles_dict = [{'name': r.name, 'role_id': r.role_id} for r in roles]
        return True, roles_dict, None
    except Exception as e:
        return False, 'bedb/get_roles', str(e)


################################
# STATIONLEAD
################################


################################
# STATIONSCORE
################################
def update_station_scores(event_id, team_scores):
    try:
        for gs_id in team_scores:
            for team_id in team_scores[gs_id]:
                for round_number in team_scores[gs_id][team_id]:
                    st_score = StationScore.ByKeys(event_id, gs_id, team_id, round_number)
                    st_score.score = team_scores[gs_id][team_id][round_number]
        TioDB.commit()
        return True, None, None
    except Exception as e:
        return False, 'bedb/update-stationscore-failed', str(e)


def get_station_team_placements(event, game):
    # todo: score_type muss berücksichtigt werden, wir gehen aktuell erstmal von punkten aus

    if isinstance(event, str):
        event = Event.ByKeys(event_id=event)

    if isinstance(game, str):
        game = Games.KeywordQuery(game_id=game)[0]

    team_placements_dict = defaultdict(int)
    team_placements = []
    game_stations = GameStation.KeywordQuery(event_id=event.event_id, game_id=game.game_id)

    counting_type = {
        'Aufsteigend': 0,
        'Abfallend': 1
    }
    ascending = counting_type[game.score_counting] == 1

    for gs in game_stations:
        station_scores = StationScore.KeywordQuery(
            event_id=event.event_id,
            game_station_id=gs.game_station_id,
            team_id=gs.team_a_id
        )

        for s_score in station_scores:
            if s_score.score:
                team_placements_dict[gs.team_a_id] += s_score.score

        station_scores = StationScore.KeywordQuery(
            event_id=event.event_id,
            game_station_id=gs.game_station_id,
            team_id=gs.team_b_id
        )

        for s_score in station_scores:
            if s_score.score:
                team_placements_dict[gs.team_b_id] += s_score.score

    for team_id, team_score in team_placements_dict.items():
        team_placements.append({
            'placement': 0,
            'team_id': team_id,
            'team_score': team_score,
            'team_name': Team.ByKeys(team_id=team_id).name,
            'team_number': Team.ByKeys(team_id=team_id).number
        })

    if team_placements:
        team_placements.sort(key=lambda x: x['team_score'], reverse=not ascending)

        # making sure, that teams with same score have same placement
        current_placement = 1
        num_teams = len(team_placements)
        previous_score = team_placements[0]['team_score']
        team_placements[0]['placement'] = current_placement
        team_placements[0]['score_points'] = num_teams

        for i in range(1, num_teams):
            score_points = num_teams - i
            if team_placements[i]['team_score'] == previous_score:
                team_placements[i]['placement'] = current_placement
                team_placements[i]['score_points'] = score_points
            else:
                current_placement += 1
                team_placements[i]['placement'] = current_placement
                team_placements[i]['score_points'] = score_points
                previous_score = team_placements[i]['team_score']

    # todo: fehler handling einbauen
    return True, team_placements, None


################################
# TEAM
################################
def update_teams_names(teams):
    all_teams = []
    for team_id, team_values in teams.items():
        # teams without names should not be changed into empty names in case of
        # team name is change in another station
        if not team_values.get('name'):
            continue
        _t = Team.ByKeys(team_id=team_id)
        if _t:
            all_teams.append(_t)
            _t.name = team_values['name']

    TioDB.add_objects(all_teams)

    return True, None, None


################################
# USER
################################
def check_user_exist(user_login):
    if User.ByKeys(user_login):
        return True
    return False


def create_user(user, password, roles):
    new_user = User(
        # todo: if user id works via constructor, this line can be removed
        user_id=tools.generate_id(tioglobals.TIO_USER),
        **user
    )

    new_user_pw = UserPW(user_id=new_user.user_id, user_pw=tools.hash_pw(password))
    user_roles = []
    for role in roles:
        user_roles.append(UserRoles(user_id=new_user.user_id, role_id=role['role_id']))

    try:
        TioDB.add_objects([new_user, new_user_pw] + user_roles)
    except sqlalchemy.exc.IntegrityError as err:
        return False, 'db_error', str(err)
    except Exception as err:
        return False, 'unknown_error', str(err)

    return new_user, None, None


def update_user(user, data):
    if user:
        # todo: checken, ob essentielle daten wie vorname, etc. geändert werden dürfen
        # todo: robuster gestalten. bspw. mit .get
        user.firstname = data['firstname']
        user.lastname = data['lastname']
        user.email = data['email']
        user.phone = data['phone']
        user.gender = data['gender']
        user.title = data['title']
        user.function = data['function']

        if data.get('profileBlobId'):
            user.profile_blob_id = data['profileBlobId']

        if data.get('roles'):
            update_user_roles(data.get('userId'), data['roles'])

        blob_id = data.get('userProfilePictureBlobId')
        blob_date = data.get('userProfilePictureBlobUploadDate')
        if blob_id:
            user.profile_blob_id = blob_id
            blob = Blobstore.ByKeys(blob_id)
            blob.object_id = user.user_id
            blob.blob_upload_date = tools.parse_date(blob_date)

        try:
            TioDB.commit()
        except sqlalchemy.exc.IntegrityError as err:
            return False, 'db_error', str(err)

        return True, 'user/update-success', None

    return False, 'user/user-not-found', 'Kritisch: User wurde nicht gefunden. Bitte an IT wenden.'


def get_user_object(user_id):
    return User.KeywordQuery(user_id=user_id)[0]


def remove_first_login_flag(user):
    user.first_login = 0
    user.commit()


def change_user_account_status(user, active):
    try:
        user.active = active
        user.commit()
        return True, 'user/status_change-success', None
    except sqlalchemy.exc.IntegrityError as err:
        return False, 'user/status_change-failed', str(err)


# USERPICTURES


################################
# USERPW
################################
def check_login(user, password):
    # todo: auch pruefen, ob user aktiv ist
    user_pw = UserPW.ByKeys(user.user_id)
    return bcrypt.checkpw(PW_STRING.format(password).encode(), user_pw.user_pw)


def create_user_session_tokens(user):
    dt = datetime.now()
    # todo: den token individuellere zusammensetzungen geben
    access_token = bcrypt.hashpw(f'{TIO_API_ACCESS_KEY}-{user.user_id}-{dt}-{user.login}'.encode(), bcrypt.gensalt())
    refresh_token = bcrypt.hashpw(f'{TIO_API_REFRESH_KEY}-{user.user_id}-{dt}-{user.login}'.encode(), bcrypt.gensalt())
    session_id = bcrypt.hashpw(f'{TIO_API_APP_KEY}-{user.user_id}-{dt}-{user.login}'.encode(), bcrypt.gensalt())

    user_session = UserSession(
        user_id=user.user_id,
        access_token=access_token,
        access_token_date=dt,
        refresh_token=refresh_token,
        refresh_token_date=dt,
        last_login=dt,
        session_id=session_id
    )
    TioDB.add_object(user_session)

    return refresh_token, access_token, session_id


def create_access_token(session_id):
    dt = datetime.now()
    """
        when a user accesses the site with a valid refresh token, he is able to get an access token.
        when retrieving an access token, the token dates will be updated
    """
    # todo: den token individuellere zusammensetzungen geben
    user_session = UserSession.KeywordQuery(session_id=session_id)
    user = User.ByKeys(user_session.user_id)
    access_token = bcrypt.hashpw(f'{TIO_API_ACCESS_KEY}-{user.user_id}-{dt}-{user.login}'.encode(), bcrypt.gensalt())

    user_session.access_token_token = access_token
    user_session.access_token_date = dt
    user_session.refresh_token_date = dt
    TioDB.db.session.commit()

    return access_token


def update_user_pw(user, pw):
    user_pw = UserPW.ByKeys(user_id=user.user_id)
    user_pw.update_pw(pw)
    return True, 'user/pw-updated', None


################################
# USERROLES
################################
def get_users_roles(user_ids):

    if isinstance(user_ids, str):
        user_ids = [user_ids]

    roles = dict()
    for user_id in user_ids:
        temp_roles = []
        user_roles = UserRoles.KeywordQuery(user_id=user_id)
        for user_role in user_roles:
            temp_roles.append(Roles.ByKeys(user_role.role_id))
        roles[user_id] = [{'name': r.name, 'role_id': r.role_id} for r in temp_roles]

    return roles


def get_user_roles(user_id):
    user_roles = UserRoles.KeywordQuery(user_id=user_id)

    roles = []
    for user_role in user_roles:
        role = Roles.ByKeys(user_role.role_id)
        roles.append({'name': role.name, 'role_id': role.role_id})

    return roles if roles else None


def update_user_roles(user_id, roles):
    role_ids = [r.get('role_id') for r in roles]
    new_user_roles = []
    for role_id in role_ids:
        if not UserRoles.ByKeys(user_id=user_id, role_id=role_id):
            new_user_roles.append(UserRoles(user_id=user_id, role_id=role_id))

    TioDB.add_objects(new_user_roles)


# USERSESSION
