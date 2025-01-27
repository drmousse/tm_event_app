import itertools
import random


def generate_visit_schedule(n):
    # Initialize the schedule matrix
    schedule = [[0] * n for _ in range(n)]
    # Create a list of groups as letters
    groups = [chr(65 + i) for i in range(n)]

    for round in range(n):
        for group_index in range(n):
            # Calculate the station for the current group in the current round
            station = (group_index + round) % n
            schedule[round][group_index] = groups[station]

    return schedule


def generate_tournament_schedule(n, m):
    if n * (n - 1) // 2 < m * (n // 2):
        raise ValueError("Not enough possible matchups to satisfy the conditions.")

    # Generate all possible pairs of teams
    teams = list(range(1, n + 1))
    all_pairs = list(itertools.combinations(teams, 2))

    # Shuffle pairs to randomize the schedule
    random.shuffle(all_pairs)

    # Initialize the schedule for each game
    schedule = [[] for _ in range(m)]
    used_pairs = set()

    for game_index in range(m):
        game_pairs = []
        teams_in_game = set()

        # Generate pairs for the current game
        for pair in all_pairs:
            if pair not in used_pairs and pair[0] not in teams_in_game and pair[1] not in teams_in_game:
                game_pairs.append(pair)
                teams_in_game.update(pair)
                used_pairs.add(pair)

            if len(teams_in_game) == n:
                break

        if len(teams_in_game) < n:
            raise ValueError("Failed to generate a valid schedule with the given constraints.")

        schedule[game_index] = game_pairs

    return schedule


def run_generate_visit_schedule():
    n = 3  # Number of stations (and groups)
    schedule = generate_visit_schedule(n)
    for round, visits in enumerate(schedule):
        print(f"Round {round + 1}: {visits}")


def run_generate_tournament_schedule():
    n = 4  # Number of teams
    m = 3  # Number of games
    num_groups = 3
    schedule_generated = False
    while not schedule_generated:
        try:
            schedule = generate_tournament_schedule(n, m)
            schedule_generated = True
        except Exception:
            pass
    for j in range(num_groups):
        print(f"gruppe { chr(j+65)}")
        for i, game in enumerate(schedule):
            print(f"Game {i + 1}: {game[0][0] + j*n}-{game[0][1] + j*n}, "
                  f"{game[1][0] + j*n}-{game[1][1] + j*n}")


if __name__ == '__main__':
    run_generate_visit_schedule()
    run_generate_tournament_schedule()
