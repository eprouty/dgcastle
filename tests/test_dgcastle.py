import unittest
from dgcastle import dgcastle

class TestInputMethods(unittest.TestCase):

    def test_CanInputRound(self):
        try:
            dgcastle.inputRound()
        except:
            self.fail("Could not input round")

if __name__ == '__main__':
    unittest.main()
