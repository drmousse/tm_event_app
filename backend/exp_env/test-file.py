import random
import copy
from collections import defaultdict
from datetime import datetime
from itertools import permutations, combinations


def already_played_with(team, opponent, game_distro):
    for game, enemy in game_distro[team].values():
        if enemy == opponent:
            return True
    return False


def game_already_played(team, game, game_distro):
    for g, o in game_distro[team].values():
        if g == game:
            return True
    return False


def game_round_slots_full(rnd, game, game_distro):
    counter = 0
    for team, distro in game_distro.items():
        if distro.get(rnd):
            if distro.get(rnd)[0] == game:
                counter += 1
        if counter == 2:
            return True
    return False


def assign_game(team_distro_occupation, team, rnd, game, opponent):
    team_distro_occupation[team][rnd] = [game, opponent]
    team_distro_occupation[opponent][rnd] = [game, team]


def remove_game(team_distro_occupation, team, rnd):
    opponent = team_distro_occupation[team][rnd][1]
    del team_distro_occupation[team][rnd]
    del team_distro_occupation[opponent][rnd]


def backtracking(team_distro_occupation, all_rounds, all_games, all_teams, game_counts, idx=0):
    if idx == len(all_rounds) * len(all_teams):
        return all(len(game_counts[team]) == len(all_games) for team in all_teams)

    rnd_idx = idx // len(all_teams)
    team_idx = idx % len(all_teams)
    rnd = all_rounds[rnd_idx]
    team = all_teams[team_idx]

    if team_distro_occupation[team].get(rnd):
        return backtracking(team_distro_occupation, all_rounds, all_games, all_teams, game_counts, idx + 1)

    random.shuffle(all_games)
    random.shuffle(all_teams)

    for game in all_games:
        if game in game_counts[team]:
            continue

        for opponent in all_teams:
            if team == opponent:
                continue
            if already_played_with(team, opponent, team_distro_occupation):
                continue
            if game_already_played(team, game, team_distro_occupation):
                continue
            if game_already_played(opponent, game, team_distro_occupation):
                continue
            if game_round_slots_full(rnd, game, team_distro_occupation):
                continue
            if team_distro_occupation[opponent].get(rnd):
                continue
            if game in game_counts[opponent]:
                continue

            assign_game(team_distro_occupation, team, rnd, game, opponent)
            game_counts[team].add(game)
            game_counts[opponent].add(game)
            if backtracking(team_distro_occupation, all_rounds, all_games, all_teams, game_counts, idx + 1):
                return True
            game_counts[team].remove(game)
            game_counts[opponent].remove(game)
            remove_game(team_distro_occupation, team, rnd)

    return False


def create_team_distribution():
    random.seed(int(datetime.now().timestamp()))
    all_rounds = ['R1', 'R2', 'R3']
    all_games = ['G1', 'G2', 'G3']
    all_teams = [1, 2, 3, 4, 5, 6]

    team_distro_occupation = {team_no: {} for team_no in all_teams}
    game_counts = {team: set() for team in all_teams}

    if not backtracking(team_distro_occupation, all_rounds, all_games, all_teams, game_counts):
        raise ValueError("No valid distribution found.")

    for k, v in team_distro_occupation.items():
        print(k, v)


def test_my_func1():
    def simpleNRooks(size, rounds, schedule):
        ''' Place n rooks on board so that they don't hit each other in each round,
            nor reuse the spots from previous rounds '''
        for i in range(size):
            for j in range(rounds):
                if size - j * 2 - i - 1 < 0:
                    schedule[i][2 * size - j * 2 - i - 1] = j + 1
                else:
                    schedule[i][size - j * 2 - i - 1] = j + 1

    # parameters
    teams = 6
    matches = 3

    # prepare the schedule, 0's designate free space
    schedule = [[0 for i in range(teams)] for j in range(teams)]

    simpleNRooks(teams, matches, schedule)

    print('Final schedule')
    for i in range(teams):
        print(schedule[i])


if __name__ == '__main__':
    create_team_distribution()
