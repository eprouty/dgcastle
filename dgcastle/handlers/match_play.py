from dgcastle.data.match import Match

class MatchPlay():
    def input_match_play(self, matches):
        if not isinstance(matches, list):
            matches = [matches]

        for match in matches:
            match.insert(self.db)

    def get_result(self, player1, player2):
        return Match('Player1', 'Player2', '2&1')

    def get_results(self, player):
        results = []
        for match in self.db.match_play.find({'winner': player}):
            results.append(Match(dbRecord=match))
        
        for match in self.db.match_play.find({'loser': player}):
            results.append(Match(dbRecord=match))

        return results