class Match():
    def __init__(self, winner='', loser='', result='', dbRecord=None):
        if dbRecord:
            self.winner = dbRecord['winner']
            self.loser = dbRecord['loser']
            self.result = dbRecord['result']
        else:
            self.winner = winner
            self.loser = loser
            self.result = result

    def __eq__(self, other):
        return self.winner == other.winner and self.loser == other.loser and self.result == other.result

    def insert(self, db):
        db.match_play.insert_one({'winner': self.winner,
                                  'loser': self.loser,
                                  'result': self.result})