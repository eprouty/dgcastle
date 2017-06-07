import unittest

from dgcastle import dgcastle
from dgcastle.data import match

matchFixture1 = match.Match('Player1', 'Player2', '2&1')
matchFixture2 = match.Match('Player3', 'Player1', '1up')

class TestInputMethods(unittest.TestCase):
    def setUp(self):
        self.dgcastle = dgcastle.DGCastle(testDb="TestInputMethods")

    def tearDown(self):
        del(self.dgcastle)

    def test_canInputMatchPlay(self):
        self.dgcastle.matchplay_input([matchFixture1])
        self.assertEqual([matchFixture1], self.dgcastle.matchplay_results('Player1'))

    def test_canInputMultipleMatches(self):
        self.dgcastle.matchplay_input([matchFixture1, matchFixture2])
        self.assertEqual(self.dgcastle.db.match_play.count(), 2)

    def test_canImportCSV(self):
        self.dgcastle.matchplay_csv("tests/fixtures/simple_matchplay.csv")
        self.assertEqual(self.dgcastle.db.match_play.count(), 5)

    def test_importLongCSV(self):
        self.dgcastle.matchplay_csv("tests/fixtures/partial_goat_results.csv")
        self.assertEqual(self.dgcastle.db.match_play.count(), 71)

class TestReadMethods(unittest.TestCase):
    def setUp(self):
        self.dgcastle = dgcastle.DGCastle(testDb="TestReadMethods")
        self.dgcastle.matchplay_input(matchFixture1)
        self.dgcastle.matchplay_input(matchFixture2)

    def tearDown(self):
        del(self.dgcastle)

    def test_findResultsForPlayer1(self):
        results = self.dgcastle.matchplay_results('Player1')
        self.assertEqual(results, [matchFixture1, matchFixture2])

    def test_findResultsForPlayer2(self):
        results = self.dgcastle.matchplay_results('Player2')
        print(matchFixture1)  # Make sure to cover the __repr__ function too
        self.assertEqual(results, [matchFixture1])

if __name__ == '__main__':
    unittest.main()
