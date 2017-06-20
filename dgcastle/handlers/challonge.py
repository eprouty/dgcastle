import challonge
import os

from dgcastle.data.match import Match
from dgcastle.data.tournament import Tournament
from dgcastle.exceptions import ValidationException, IncompleteException


class Challonge():
    """ In order to use this handler a CHALLONGE_API env variable must be set using
    your account in the format "username,KEY"
    """

    def __init__(self):
        if os.environ.get('CHALLONGE_API'):
            username, key = os.environ.get('CHALLONGE_API').split(',')
            challonge.set_credentials(username, key)

    def challonge_import(self, tournamentId):
        tournament_data = challonge.tournaments.show(tournamentId)

        # Make sure this tournament is completed before we import it
        if tournament_data['state'] != 'complete':
            raise IncompleteException("This Challonge bracket has not been marked as ended")
        
        tournament = Tournament(challongeData=tournament_data)
        participants = {}
        for participant in challonge.participants.index(tournament.id):
            # Need to make a player for each of these and put them into a dict
            # based on their ID so we can tie it back to the matches later
            tournament.add_participant(participant)


        for match in challonge.matches.index(tournament.id):
            # Need to build up a Match object for each of these and arrange them corrently into a
            # Tournament object
            p1_id = match['player1-id']
            p1 = tournament.get_participant(p1_id)
            p2_id = match['player2-id']
            p2 = tournament.get_participant(p2_id)
            result = match['scores-csv']
            winner = match['winner-id']

            if ',' in result:
                # Multiple scores were submitted for this match
                raise ValidationException("Multiple scores were submitted for the match bettwen {} and {}")
            
            winner, loser = [p1, p2] if winner == p1_id else [p2, p1]

            tournament.add_match(Match(winner=winner, loser=loser, result=result))
            
        return tournament
