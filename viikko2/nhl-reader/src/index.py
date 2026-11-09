from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from player_reader import PlayerReader
from player_stats import PlayerStats

def get_nationalities(players):
    base_nationalities = [
        "USA", "FIN", "CAN", "SWE", "CZE", "RUS", "SLO", "FRA", "GBR", "SVK",
        "DEN", "NED", "AUT", "BLR", "GER", "SUI", "NOR", "UZB", "LAT", "AUS",
    ]

    nationalities = [n for n in base_nationalities if n in {p.nationality for p in players}]
    for player in players:
        if player.nationality not in nationalities:
            nationalities.append(player.nationality)

    return nationalities or base_nationalities


def display_table(console, season, nationality, players):
    table = Table(title=f"Season {season} players from {nationality}")
    columns = [
        ("Released", {"style": "cyan", "no_wrap": True}),
        ("teams", {"style": "magenta"}),
        ("goals", {"justify": "right", "style": "green"}),
        ("assists", {"justify": "right", "style": "green"}),
        ("points", {"justify": "right", "style": "green"}),
    ]
    for name, kwargs in columns:
        table.add_column(name, **kwargs)

    for player in players:
        table.add_row(
            player.name,
            player.team,
            str(player.goals),
            str(player.assists),
            str(player.goals + player.assists),
        )

    console.print(table)


def query_nationalities(console, stats, season, nationalities):
    while True:
        nationality = Prompt.ask("Nationality", choices=nationalities, default="")
        if not nationality:
            break

        players = stats.top_scorers_by_nationality(nationality)
        display_table(console, season, nationality, players)


def main():
    console = Console()

    seasons = [
        "2018-19",
        "2019-20",
        "2020-21",
        "2021-22",
        "2022-23",
        "2023-24",
        "2024-25",
        "2025-26",
    ]

    season = Prompt.ask("Season", choices=seasons, default="2024-25")
    url = f"https://studies.cs.helsinki.fi/nhlstats/{season}/players"
    stats = PlayerStats(PlayerReader(url))

    nationalities = get_nationalities(stats.players)
    query_nationalities(console, stats, season, nationalities)

if __name__ == "__main__":
    main()
