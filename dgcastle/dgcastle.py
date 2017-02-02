'''DGCastle: A disc golf statistics tracking tool'''
import collections
MatchPlay = collections.namedtuple('MatchPlay', ['winner', 'loser', 'result'])

STATE = []

def input_match_play(matches):
    if not isinstance(matches, list):
        matches = [matches]

    for match in matches:
        STATE.append(MatchPlay(match[0], match[1], match[2]))

def get_result(player1, player2):
    return MatchPlay('Player1', 'Player2', '2&1')

def get_results(player):
    results = [x for x in STATE if (x.winner == player or x.loser == player)]
    return results
