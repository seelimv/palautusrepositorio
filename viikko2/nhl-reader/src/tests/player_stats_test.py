import unittest

from player import Player
from player_stats import PlayerStats


class PlayerReaderStub:
    def get_players(self):
        return [
            Player({
                "name": "Semenko",
                "nationality": "CAN",
                "team": "EDM",
                "goals": 4,
                "assists": 12,
            }),
            Player({
                "name": "Lemieux",
                "nationality": "CAN",
                "team": "PIT",
                "goals": 45,
                "assists": 54,
            }),
            Player({
                "name": "Kurri",
                "nationality": "FIN",
                "team": "EDM",
                "goals": 37,
                "assists": 53,
            }),
            Player({
                "name": "Yzerman",
                "nationality": "CAN",
                "team": "DET",
                "goals": 42,
                "assists": 56,
            }),
        ]


class TestPlayerStats(unittest.TestCase):
    def setUp(self):
        self.stats = PlayerStats(PlayerReaderStub())

    def test_top_scorers_by_nationality_returns_players_in_points_order(self):
        players = self.stats.top_scorers_by_nationality("CAN")

        self.assertEqual(["Lemieux", "Yzerman", "Semenko"], [
            player.name for player in players
        ])

    def test_top_scorers_by_team_returns_players_in_points_order(self):
        players = self.stats.top_scorers_by_team("EDM")

        self.assertEqual(["Kurri", "Semenko"], [
            player.name for player in players
        ])

    def test_top_goal_scorers_returns_requested_number_in_goal_order(self):
        players = self.stats.top_goal_scorers(2)

        self.assertEqual(["Lemieux", "Yzerman"], [
            player.name for player in players
        ])


if __name__ == "__main__":
    unittest.main()
