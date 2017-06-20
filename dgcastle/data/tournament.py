from dgcastle.data.player import Player

class Tournament():
    def __init__(self, challongeData=None):
        self.id = challongeData['id']
        self.url = challongeData['full-challonge-url']
        self.started = challongeData['created-at']
        self.completed = challongeData['completed-at']
        self.participants = {}
        self.matches = []

    def add_match(self, match):
        self.matches.append(match)

    def add_participant(self, participant):
        self.participants[participant['id']] = Player(participant['display-name'])  # FIXME: This should almost certainly be a PlayerFactory that will do a bit of leg work in order to pick the correct player reference based on the given name

    def get_participant(self, id):
        return self.participants[id]