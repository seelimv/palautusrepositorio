from player_reader import PlayerReader
from player_stats import PlayerStats
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table


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
    reader = PlayerReader(url)
    stats = PlayerStats(reader)

    base_nationalities = [
        "USA", "FIN", "CAN", "SWE", "CZE", "RUS", "SLO", "FRA", "GBR", "SVK",
        "DEN", "NED", "AUT", "BLR", "GER", "SUI", "NOR", "UZB", "LAT", "AUS",
    ]

    nationalities = [n for n in base_nationalities if n in {p.nationality for p in stats.players}]
    for player in stats.players:
        if player.nationality not in nationalities:
            nationalities.append(player.nationality)

    if not nationalities:
        nationalities = base_nationalities

    while True:
        nationality = Prompt.ask("Nationality", choices=nationalities, default="")
        if not nationality:
            break

        players = stats.top_scorers_by_nationality(nationality)

        table = Table(title=f"Season {season} players from {nationality}")
        table.add_column("Released", style="cyan", no_wrap=True)
        table.add_column("teams", style="magenta")
        table.add_column("goals", justify="right", style="green")
        table.add_column("assists", justify="right", style="green")
        table.add_column("points", justify="right", style="green")

        for player in players:
            table.add_row(
                player.name,
                player.team,
                str(player.goals),
                str(player.assists),
                str(player.goals + player.assists),
            )

        console.print(table)

if __name__ == "__main__":
    main()
