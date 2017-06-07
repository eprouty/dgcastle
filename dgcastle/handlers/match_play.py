import csv

from dgcastle.data.match import Match

class HeaderException(Exception):
    """Raises concerns about the way you've formatted your csv files."""

class MatchPlay():
    def matchplay_input(self, matches):
        if not isinstance(matches, list):
            matches = [matches]

        for match in matches:
            match.insert(self.db)

    def matchplay_csv(self, csvLoc):
        winnerCol = None
        loserCol = None
        resultCol = None
        with open(csvLoc, newline='') as csvFile:
            matchReader = csv.reader(csvFile)
            row = next(matchReader)
            for i, header in enumerate(row):
                if header.lower().strip() == 'winner':
                    winnerCol = i
                elif header.lower().strip() == 'loser':
                    loserCol = i
                elif header.lower().strip() == 'result':
                    resultCol = i
            
            if None in [winnerCol, loserCol, resultCol]:
                raise HeaderException("Matchplay csv record is missing proper headers.\nRequires: 'winner', 'loser', 'result'")
            for row in matchReader:
                self.matchplay_input(Match(row[winnerCol], row[loserCol], row[resultCol]))

    def matchplay_results(self, player):
        results = []
        for match in self.db.match_play.find({'winner': player}):
            results.append(Match(dbRecord=match))
        
        for match in self.db.match_play.find({'loser': player}):
            results.append(Match(dbRecord=match))

        return results