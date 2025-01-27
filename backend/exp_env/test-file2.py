import random
import copy
from collections import defaultdict
from datetime import datetime
import itertools


def check_round_slots_occupied(rnd, game_distro, num_slots):
    counter = 0
    for team, distro in game_distro.items():
        if distro.get(rnd):
            counter += 1

    return counter == num_slots


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


def create_team_distirbution():

    random.seed(int(datetime.now().timestamp()))
    all_rounds = ['R1', 'R2', 'R3', 'R4']
    all_games = ['G1', 'G2', 'G3', 'G4']
    all_teams = [1, 2, 3, 4, 5, 6, 7, 8]
    all_opponents = copy.deepcopy(all_teams)

    # set up distribution
    team_distro_occupation = {}
    for team_no in range(1, len(all_teams)+1):
        team_distro_occupation[team_no] = {}


    random.shuffle(all_rounds)
    for idx, rnd in enumerate(all_rounds):
        random.shuffle(all_teams)
        random.shuffle(all_games)
        while not check_round_slots_occupied(rnd, team_distro_occupation, len(all_rounds) * 2):
            for game in all_games:
                for team in all_teams:
                    if team_distro_occupation[team].get(rnd):
                        continue

                    opponent_not_found = True
                    while opponent_not_found:
                        random.shuffle(all_opponents)
                        for opponent in all_opponents:

                            if team == opponent:
                                continue
                            if not already_played_with(team, opponent, team_distro_occupation):
                                if team_distro_occupation[opponent].get(rnd):
                                    if opponent == all_opponents[-1]:
                                        opponent_not_found = False
                                    continue
                                if game_already_played(team, game, team_distro_occupation):
                                    opponent_not_found = False
                                    break

                                if game_already_played(opponent, game, team_distro_occupation):
                                    if opponent == all_opponents[-1]:
                                        opponent_not_found = False
                                    continue

                                if game_round_slots_full(rnd, game, team_distro_occupation):
                                    opponent_not_found = False
                                    break

                                team_distro_occupation[team][rnd] = [game, opponent]
                                team_distro_occupation[opponent][rnd] = [game, team]
                                opponent_not_found = False
                                break

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
    teams = 10
    matches = 5

    # prepare the schedule, 0's designate free space
    schedule = [[0 for i in range(teams)] for j in range(teams)]

    simpleNRooks(teams, matches, schedule)

    print('Final schedule')
    for i in range(teams):
        print(schedule[i])



def round_robin(num_teams):
    """Generate a round-robin schedule for num_teams teams."""
    if num_teams % 2:
        num_teams += 1
    schedule = []
    for i in range(num_teams - 1):
        round = []
        for j in range(num_teams // 2):
            t1 = (i + j) % (num_teams - 1)
            t2 = (num_teams - 1 - j + i) % (num_teams - 1)
            if j == 0:
                t2 = num_teams - 1
            round.append((t1 + 1, t2 + 1))
        schedule.append(round)
    return schedule


def create_schedule(num_teams, num_stations):
    if num_teams != 2 * num_stations:
        raise ValueError("Number of teams must be twice the number of stations.")

    teams = list(range(1, num_teams + 1))
    rounds = num_stations
    schedule = defaultdict(list)

    # Generate round-robin pairs
    matches = round_robin(num_teams)

    # Ensure each team plays at each station exactly once
    station_assignments = defaultdict(lambda: defaultdict(bool))
    for round_number in range(1, rounds + 1):
        round_matches = []
        random.shuffle(matches[round_number - 1])
        for station, match in enumerate(matches[round_number - 1], start=1):
            team1, team2 = match
            while station_assignments[team1][station] or station_assignments[team2][station]:
                random.shuffle(matches[round_number - 1])
                match = matches[round_number - 1][station - 1]
                team1, team2 = match
            station_assignments[team1][station] = True
            station_assignments[team2][station] = True
            round_matches.append((station, team1, team2))
        schedule[round_number] = round_matches

    return schedule




if __name__ == '__main__':

    # Example usage:
    #num_teams = 6  # Must be twice the number of stations
    #num_stations = 3
    #schedule = create_schedule(num_teams, num_stations)

    #for round_number, matches in schedule.items():
    #    print(f"Round {round_number}:")
    #    for station, team1, team2 in matches:
    #        print(f"  Station {station}: Team {team1} vs Team {team2}")

    create_team_distirbution()
