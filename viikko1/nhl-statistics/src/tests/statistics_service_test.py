import unittest

from player import Player
from statistics_service import SortBy, StatisticsService


class PlayerReaderStub:
    def get_players(self):
        return [
            Player("Semenko", "EDM", 4, 12),  #  4+12 = 16
            Player("Lemieux", "PIT", 45, 54), # 45+54 = 99
            Player("Kurri",   "EDM", 37, 53), # 37+53 = 90
            Player("Yzerman", "DET", 42, 56), # 42+56 = 98
            Player("Gretzky", "EDM", 35, 89)  # 35+89 = 124
        ]

class TestStatisticsService(unittest.TestCase):
    def setUp(self):
        self.stats = StatisticsService(
            PlayerReaderStub()
        )

    def test_search_player(self):
        player = self.stats.search("Kurri")

        self.assertEqual(str(player), "Kurri EDM 37 + 53 = 90")

    def test_search_invalid_player(self):
        player = self.stats.search("invalid")

        self.assertEqual(player, None)

    def test_team(self):
        team = self.stats.team("EDM")

        self.assertTrue(team[0].name == "Semenko")

    def test_top(self):
        top_scores = self.stats.top(3)

        self.assertEqual(top_scores[0].name, "Gretzky")

    def test_sort_by_goals(self):
        top_goal_scorers = self.stats.top(3, SortBy.GOALS)

        self.assertEqual(top_goal_scorers[0].name, "Lemieux")

    def test_sort_by_assists(self):
        top_assist_scorers = self.stats.top(3, SortBy.ASSISTS)

        self.assertEqual(top_assist_scorers[0].name, "Gretzky")
