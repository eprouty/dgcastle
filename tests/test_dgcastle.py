import unittest
from dgcastle import dgcastle
from dgcastle.data import match

matchFixture1 = match.Match('Player1', 'Player2', '2&1')
matchFixture2 = match.Match('Player3', 'Player1', '1up')

class TestInputMethods(unittest.TestCase):
    def setUp(self):
        self.dgcastle = dgcastle.DGCastle(testDb="TestInputMethods")

    def test_canInputMatchPlay(self):
        self.dgcastle.input_match_play([matchFixture1])
        self.assertEqual(matchFixture1, self.dgcastle.get_result('Player1', 'Player2'))

    def test_canInputMultipleMatches(self):
        self.dgcastle.input_match_play([matchFixture1, matchFixture2])
        self.assertEqual(self.dgcastle.db.match_play.count(), 2)

    def tearDown(self):
        del(self.dgcastle)

class TestReadMethods(unittest.TestCase):
    def setUp(self):
        self.dgcastle = dgcastle.DGCastle(testDb="TestReadMethods")
        self.dgcastle.input_match_play(matchFixture1)
        self.dgcastle.input_match_play(matchFixture2)

    def tearDown(self):
        del(self.dgcastle)

    def test_findResultOfMatch(self):
        result = self.dgcastle.get_result('Player1', 'Player2')
        self.assertEqual(result, matchFixture1)
        self.assertEqual('Player1', result.winner)
        self.assertEqual('Player2', result.loser)
        self.assertEqual('2&1', result.result)

    def test_findResultForOppositePlayer(self):
        result = self.dgcastle.get_result('Player2', 'Player1')
        self.assertEqual(result, matchFixture1)

    def test_findResultsForPlayer1(self):
        results = self.dgcastle.get_results('Player1')
        self.assertEqual(results, [matchFixture1, matchFixture2])

    def test_findResultsForPlayer2(self):
        results = self.dgcastle.get_results('Player2')
        self.assertEqual(results, [matchFixture1])

if __name__ == '__main__':
    unittest.main()
