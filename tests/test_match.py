import unittest

from dgcastle.data import match
from dgcastle.exceptions import ValidationException

class TestResultValidation(unittest.TestCase):
    def test_tie(self):
        self.assertEqual(match._validate_result('tie'), 'tie')
        self.assertEqual(match._validate_result('as'), 'as')

    def test_XupFormat(self):
        self.assertEqual(match._validate_result('1up'), '1up')
        self.assertEqual(match._validate_result('2up'), '2up')
        self.assertRaises(ValidationException, match._validate_result, '0up')
        self.assertRaises(ValidationException, match._validate_result, '3up')
        self.assertRaises(ValidationException, match._validate_result, '10up')
        self.assertRaises(ValidationException, match._validate_result, '-1up')
        self.assertRaises(ValidationException, match._validate_result, 'twoup')
        self.assertRaises(ValidationException, match._validate_result, 'up')
        self.assertRaises(ValidationException, match._validate_result, '1up2')
        self.assertRaises(ValidationException, match._validate_result, '1')

    def test_XandYFormat(self):
        self.assertEqual(match._validate_result('2&1'), '2&1')
        self.assertEqual(match._validate_result('3&1'), '3&1')
        self.assertRaises(ValidationException, match._validate_result, '4&1')
        self.assertEqual(match._validate_result('4&2'), '4&2')
        self.assertEqual(match._validate_result('10&8'), '10&8')
        self.assertEqual(match._validate_result('2+1'), '2+1')
        self.assertRaises(ValidationException, match._validate_result, '10&7')
        self.assertRaises(ValidationException, match._validate_result, '4&')
        self.assertRaises(ValidationException, match._validate_result, '&1')
        self.assertRaises(ValidationException, match._validate_result, '&')
        self.assertRaises(ValidationException, match._validate_result, '4')
        self.assertRaises(ValidationException, match._validate_result, '1')
        self.assertRaises(ValidationException, match._validate_result, '1&-1')
        self.assertRaises(ValidationException, match._validate_result, '4.1&1')
        self.assertRaises(ValidationException, match._validate_result, '4&1.1')
        self.assertRaises(ValidationException, match._validate_result, '3&2&1')
        self.assertRaises(ValidationException, match._validate_result, '2&+1')
        self.assertRaises(ValidationException, match._validate_result, '2+&1')

    def test_challongeFormatting(self):
        self.assertEqual(match._validate_result('2-1'), '2&1')
        self.assertEqual(match._validate_result('1-2'), '2&1')
        self.assertEqual(match._validate_result('2-0'), '2up')
        self.assertEqual(match._validate_result('0-2'), '2up')
        self.assertRaises(ValidationException, match._validate_result, '0-0')
        self.assertRaises(ValidationException, match._validate_result, '0-')
        self.assertRaises(ValidationException, match._validate_result, '-0')
        self.assertRaises(ValidationException, match._validate_result, '5-1')
        self.assertRaises(ValidationException, match._validate_result, '0--0')
        