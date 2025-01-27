#!/usr/bin/python3
# -*- coding: utf-8 -*-

# core imports
import itertools
import random

# custom imports


# FUNCTIONS
def create_event_schedule(teams, games):
    # todo: replace mockup with working algo
    event_schedule = None
    team_no_to_id = dict()

    for team in teams:
        team_no_to_id[team.number] = team.team_id

    len_games = len(games)
    len_teams = len(teams)

    if len_games == 2:
        if len_teams == 2:
            event_schedule = {
                games[0]: [
                    (team_no_to_id[1], [team_no_to_id[2]]), (None, None)
                ],
                games[1]: [
                    (None, None), (team_no_to_id[1], [team_no_to_id[2]])
                ]
            }

        elif len_teams == 4:
            event_schedule = {
                games[0]: [
                    (team_no_to_id[1], [team_no_to_id[2]]), (team_no_to_id[3], [team_no_to_id[4]])
                ],
                games[1]: [
                    (team_no_to_id[3], [team_no_to_id[4]]), (team_no_to_id[1], [team_no_to_id[2]])
                ]
            }

    elif len_games == 3:
        if len_teams == 2:
            event_schedule = {
                games[0]: [
                    (1, 2), (None, None), (None, None)
                ],
                games[1]: [
                    (None, None), (1, 2), (None, None)
                ],
                games[2]: [
                    (None, None), (None, None), (1, 2)
                ]
            }
        elif len_teams == 4:
            event_schedule = {
                games[0]: [
                    (1, 2), (3, 4), (None, None)
                ],
                games[1]: [
                    (None, None), (1, 2), (3, 4)
                ],
                games[2]: [
                    (3, 4), (None, None), (1, 2)
                ]
            }
        elif len_teams == 6:
            event_schedule = {
                games[0]: [
                    (1, 2), (3, 4), (5, 6)
                ],
                games[1]: [
                    (3, 5), (1, 6), (2, 4)
                ],
                games[2]: [
                    (4, 6), (2, 5), (1, 3)
                ]
            }

    elif len_games == 4:
        if len_teams == 2:
            event_schedule = {
                games[0]: [
                    (1, 2), (None, None), (None, None), (None, None)
                ],
                games[1]: [
                    (None, None), (1, 2), (None, None), (None, None)
                ],
                games[2]: [
                    (None, None), (None, None), (1, 2), (None, None)
                ],
                games[3]: [
                    (None, None), (None, None), (None, None), (1, 2)
                ]
            }
        elif len_teams == 4:
            event_schedule = {
                games[0]: [
                    (1, 2), (3, 4), (None, None), (None, None)
                ],
                games[1]: [
                    (None, None), (None, None), (1, 4), (2, 3)
                ],
                games[2]: [
                    (3, 4), (1, 2), (None, None), (None, None)
                ],
                games[3]: [
                    (None, None), (None, None), (2, 3), (1, 4)
                ]
            }
        elif len_teams == 6:
            event_schedule = {
                games[0]: [
                    (1, 2), (3, 4), (5, 6), (None, None)
                ],
                games[1]: [
                    (3, 5), (1, 6), (None, None), (2, 4)
                ],
                games[2]: [
                    (None, None), (2, 5), (1, 4), (3, 6)
                ],
                games[3]: [
                    (4, 6), (None, None), (2, 3), (1, 5)
                ]
            }
        elif len_teams == 8:
            event_schedule = {
                games[0]: [
                    (1, 2), (3, 4), (5, 6), (7, 8)
                ],
                games[1]: [
                    (4, 7), (1, 6), (3, 8), (2, 5)
                ],
                games[2]: [
                    (3, 5), (2, 8), (1, 7), (4, 6)
                ],
                games[3]: [
                    (6, 8), (5, 7), (2, 4), (1, 3)
                ]
            }

    elif len_games == 5:
        if len_teams == 2:
            event_schedule = {
                games[0]: [
                    (1, 2), (None, None), (None, None), (None, None), (None, None)
                ],
                games[1]: [
                    (None, None), (1, 2), (None, None), (None, None), (None, None)
                ],
                games[2]: [
                    (None, None), (None, None), (1, 2), (None, None), (None, None)
                ],
                games[3]: [
                    (None, None), (None, None), (None, None), (1, 2), (None, None)
                ],
                games[4]: [
                    (None, None), (None, None), (None, None), (None, None), (1, 2)
                ]
            }
        elif len_teams == 4:
            event_schedule = {
                games[0]: [
                    (1, 2), (3, 4), (None, None), (None, None), (None, None)
                ],
                games[1]: [
                    (None, None), (None, None), (1, 3), (2, 4), (None, None)
                ],
                games[2]: [
                    (None, None), (None, None), (2, 4), (1, 3), (None, None)
                ],
                games[3]: [
                    (None, None), (1, 2), (None, None), (None, None), (3, 4)
                ],
                games[4]: [
                    (3, 4), (None, None), (None, None), (None, None), (1, 2)
                ]
            }
        elif len_teams == 6:
            event_schedule = {
                games[0]: [
                    (1, 2), (None, None), (3, 4), (None, None), (5, 6)
                ],
                games[1]: [
                    (4, 6), (1, 5), (None, None), (2, 3), (None, None)
                ],
                games[2]: [
                    (3, 5), (None, None), (1, 6), (None, None), (2, 4)
                ],
                games[3]: [
                    (None, None), (2, 6), (None, None), (4, 5), (1, 3)
                ],
                games[4]: [
                    (None, None), (3, 4), (2, 5), (1, 6), (None, None)
                ]
            }
        elif len_teams == 8:
            event_schedule = {
                games[0]: [
                    (1, 2), (3, 4), (7, 8), (None, None), (5, 6)
                ],
                games[1]: [
                    (5, 6), (7, 8), (1, 3), (2, 4), (None, None)
                ],
                games[2]: [
                    (None, None), (5, 6), (2, 4), (1, 3), (7, 8)
                ],
                games[3]: [
                    (7, 8), (1, 2), (None, None), (5, 6), (3, 4)
                ],
                games[4]: [
                    (3, 4), (None, None), (5, 6), (7, 8), (1, 2)
                ]
            }
        elif len_teams == 10:
            event_schedule = {
                games[0]: [
                    (1, 2), (3, 4), (5, 6), (7, 8), (9, 10)
                ],
                games[1]: [
                    (3, 10), (2, 5), (4, 7), (6, 9), (1, 8)
                ],
                games[2]: [
                    (5, 8), (7, 10), (2, 9), (1, 4), (3, 6)
                ],
                games[3]: [
                    (6, 7), (8, 9), (1, 10), (2, 3), (4, 5)
                ],
                games[4]: [
                    (4, 9), (1, 6), (3, 8), (5, 10), (2, 7)
                ],
            }

    elif len_games == 6:
        if len_teams == 2:
            event_schedule = {
                games[0]: [
                    (1, 2), (None, None), (None, None), (None, None), (None, None), (None, None)
                ],
                games[1]: [
                    (None, None), (1, 2), (None, None), (None, None), (None, None), (None, None)
                ],
                games[2]: [
                    (None, None), (None, None), (1, 2), (None, None), (None, None), (None, None),
                ],
                games[3]: [
                    (None, None), (None, None), (None, None), (1, 2), (None, None), (None, None),
                ],
                games[4]: [
                    (None, None), (None, None), (None, None), (None, None), (1, 2), (None, None),
                ],
                games[5]: [
                    (None, None), (None, None), (None, None), (None, None), (None, None), (1, 2)
                ]
            }
        elif len_teams == 4:
            event_schedule = {
                games[0]: [
                    (1, 2), (3, 4), (None, None), (None, None), (None, None), (None, None)
                ],
                games[1]: [
                    (3, 4), (1, 2), (None, None), (None, None), (None, None), (None, None)
                ],
                games[2]: [
                    (None, None), (None, None), (1, 3), (2, 4), (None, None), (None, None)
                ],
                games[3]: [
                    (None, None), (None, None), (2, 4), (1, 3), (None, None), (None, None)
                ],
                games[4]: [
                    (None, None), (None, None), (None, None), (None, None), (1, 4), (2, 3)
                ],
                games[5]: [
                    (None, None), (None, None), (None, None), (None, None), (2, 3), (1, 4)
                ]
            }
        elif len_teams == 6:
            event_schedule = {
                games[0]: [
                    (1, 2), (4, 5), (None, None), (None, None), (None, None), (3, 6)
                ],
                games[1]: [
                    (None, None), (1, 3), (2, 6), (None, None), (None, None), (4, 5)
                ],
                games[2]: [
                    (None, None), (None, None), (1, 4), (3, 6), (2, 5), (None, None)
                ],
                games[3]: [
                    (None, None), (2, 6), (None, None), (1, 5), (3, 4), (None, None)
                ],
                games[4]: [
                    (3, 5), (None, None), (None, None), (2, 4), (1, 6), (None, None)
                ],
                games[5]: [
                    (4, 6), (None, None), (3, 5), (None, None), (None, None), (1, 2)
                ]
            }
        elif len_teams == 8:
            event_schedule = {
                games[0]: [
                    (1, 6), (None, None), (3, 8), (2, 5), (None, None), (4, 7)
                ],
                games[1]: [
                    (2, 8), (6, 7), (None, None), (3, 4), (1, 5), (None, None)
                ],
                games[2]: [
                    (None, None), (2, 3), (5, 7), (None, None), (4, 6), (1, 8)
                ],
                games[3]: [
                    (None, None), (None, None), (1, 4), (6, 8), (2, 7), (3, 5)
                ],
                games[4]: [
                    (3, 4), (5, 8), (None, None), (1, 7), (None, None), (2, 6)
                ],
                games[5]: [
                    (5, 7), (1, 4), (2, 6), (None, None), (3, 8), (None, None)
                ]
            }

    if event_schedule:
        transformed_event_schedule = {}
        for game, matches in event_schedule.items():
            transformed_matches = [
                (None if team1 is None and team2 is None else (team_no_to_id[team1], team_no_to_id[team2])) for
                team1, team2 in matches]
            transformed_event_schedule[game] = transformed_matches

        return transformed_event_schedule

    return event_schedule


def generate_group_schedule(num_groups):
    # Initialize the schedule matrix
    schedule = [[0] * num_groups for _ in range(num_groups)]
    # Create a list of groups as letters
    groups = [chr(65 + i) for i in range(num_groups)]

    for _round in range(num_groups):
        for group_index in range(num_groups):
            # Calculate the station for the current group in the current round
            station = (group_index + _round) % num_groups
            schedule[_round][group_index] = groups[station]

    return schedule


def generate_tournament_schedule(teams, num_pairings, num_games):
    n = len(teams)

    while True:
        try:
            if num_pairings * 2 > n:
                raise ValueError("Number of pairings per game is too high for the number of teams.")

                # Generate all possible pairs of teams
            all_pairs = list(itertools.combinations(teams, 2))

            # Shuffle pairs to randomize the schedule
            random.shuffle(all_pairs)

            # Initialize the schedule for each game
            schedule = [[] for _ in range(num_games)]
            used_pairs = set()

            for game_index in range(num_games):
                game_pairs = []
                teams_in_game = set()

                # Generate pairs for the current game
                while len(game_pairs) < num_pairings:
                    for pair in all_pairs:
                        if pair not in used_pairs and pair[0] not in teams_in_game and pair[1] not in teams_in_game:
                            game_pairs.append(pair)
                            teams_in_game.update(pair)
                            used_pairs.add(pair)
                            if len(game_pairs) == num_pairings:
                                break
                    else:
                        # Reset the used pairs to allow more combinations
                        used_pairs.clear()
                        game_pairs.clear()
                        teams_in_game.clear()
                        random.shuffle(all_pairs)

                schedule[game_index] = game_pairs

            return schedule
        except Exception:
            pass


def event_schedule_creation_possible(len_teams, len_games):
    two_games_combination = len_games == 2 and len_teams in [2, 4]
    three_games_combination = len_games == 3 and len_teams in [2, 4, 6]
    four_games_combination = len_games == 4 and len_teams in [2, 4, 6, 8]
    five_games_combination = len_games == 5 and len_teams in [2, 4, 6, 8, 10]
    six_games_combination = len_games == 6 and len_teams in [2, 4, 6, 8, 10, 12]

    return (two_games_combination
            or three_games_combination
            or four_games_combination
            or five_games_combination
            or six_games_combination)
