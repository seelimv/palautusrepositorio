from player_reader import PlayerReader
from player_stats import PlayerStats


def main():
    NATIONALITY = "FIN"
    URL = "https://studies.cs.helsinki.fi/nhlstats/2024-25/players"
    reader = PlayerReader(URL)
    stats = PlayerStats(reader)
    players = stats.top_scorers_by_nationality(NATIONALITY)

    print(f"Players from {NATIONALITY}:\n")

    for player in players:
        print(player)

if __name__ == "__main__":
    main()
