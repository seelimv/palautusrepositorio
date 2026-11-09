class Player:  # pylint: disable=too-few-public-methods
    def __init__(self, dictionary):
        self.name = dictionary['name']
        self.nationality = dictionary['nationality']
        self.assists = dictionary['assists']
        self.goals = dictionary['goals']
        self.team = dictionary['team']

    def __str__(self):
        return f"{self.name:20} {self.team:15} {self.goals:2} + {self.assists:2} = {self.goals + self.assists}"
