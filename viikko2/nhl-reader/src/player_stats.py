class PlayerStats:  # pylint: disable=too-few-public-methods
    def __init__(self, reader):
        self.players = reader.get_players()

    def top_scorers_by_nationality(self, nationality):
        players = []

        for player in self.players:
            if player.nationality == nationality:
                players.append(player)

        players.sort(key=lambda player:  player.goals + player.assists, reverse=True)

        return players

    def top_scorers_by_team(self, team):
        players = [player for player in self.players if player.team == team]
        players.sort(key=lambda player: player.goals + player.assists, reverse=True)
        return players

    def top_goal_scorers(self, how_many):
        """Palauttaa how_many eniten maaleja tehnyttä pelaajaa maalimäärän mukaan laskevassa järjestyksessä"""
        players = sorted(self.players, key=lambda player: player.goals, reverse=True)
        return players[:how_many]
