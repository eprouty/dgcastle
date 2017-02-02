import unittest
from dgcastle import dgcastle

matchFixture1 = ('Player1', 'Player2', '2&1')
matchFixture2 = ('Player3', 'Player1', '1up')

class TestInputMethods(unittest.TestCase):
    def test_canInputMatchPlay(self):
        dgcastle.input_match_play([matchFixture1])
        self.assertEqual(matchFixture1, dgcastle.get_result('Player1', 'Player2'))

    def test_canInputMultipleMatches(self):
        dgcastle.input_match_play([matchFixture1, matchFixture2])
        self.assertEqual(len(dgcastle.STATE), 2)

    def tearDown(self):
        dgcastle.STATE = []

class TestReadMethods(unittest.TestCase):
    def setUp(self):
        dgcastle.input_match_play(matchFixture1)
        dgcastle.input_match_play(matchFixture2)

    def tearDown(self):
        dgcastle.STATE = []

    def test_findResultOfMatch(self):
        result = dgcastle.get_result('Player1', 'Player2')
        self.assertEqual(result, matchFixture1)
        self.assertEqual('Player1', result.winner)
        self.assertEqual('Player2', result.loser)
        self.assertEqual('2&1', result.result)

    def test_findResultForOppositePlayer(self):
        result = dgcastle.get_result('Player2', 'Player1')
        self.assertEqual(result, matchFixture1)

    def test_findResultsForPlayer1(self):
        results = dgcastle.get_results('Player1')
        self.assertEqual(results, [matchFixture1, matchFixture2])

    def test_findResultsForPlayer2(self):
        results = dgcastle.get_results('Player2')
        self.assertEqual(results, [matchFixture1])

if __name__ == '__main__':
    unittest.main()
