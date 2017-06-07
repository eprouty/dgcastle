class ValidationException(Exception):
    """Used to report failures to validate an input format"""

def _validate_result(result):
        """Matchplay results can have 1 of 3 different types of values...
            1. A victory that ended before all 18 holes were played
                "<X>&<Y> where X > 1 and X > Y >= 1 and X - Y <= 2
            2. A victory that ended at 18 holes
                "<X>up" where 0 < X < 3
            3. A tie or "all square"
                a. "tie" or "as"
        """
        if '.' in result:
            raise ValidationException("Result '{}' should not contain decimals".format(result))
        elif result in ['tie', 'as']:
            # Simplest case, already valid, good to go
            pass
        elif "up" in result:
            tmp = result.split("up")
            if len(tmp) != 2 or tmp[1] != '':
                # We've got extra info here
                raise ValidationException("Result '{}' not in the format 'Xup'".format(result))
            try:
                tmp = int(tmp[0])
                if 0 < tmp < 3:
                    # we're good here
                    pass
                else:
                    raise ValueError()
            except ValueError:
                raise ValidationException("Result '{}' must start with an integer of value 1 or 2".format(result))
        elif "&" in result:
            tmp = result.split("&")
            if len(tmp) != 2:
                # We've got extra info here
                raise ValidationException("Result '{}' not in the format 'X&Y'".format(result))
            try:
                X = int(tmp[0])
                Y = int(tmp[1])
                if X > 1  and X > Y >= 1 and X - Y <= 2:
                    # we're good here
                    pass
                else:
                    raise ValidationException("Result '{}' is not a valid score. Given the format 'X&Y' must have X > 1 and X > Y >= 1".format(result))
            except ValueError:
                raise ValidationException("Result '{}' must use integers".format(result))
        else:
            raise ValidationException("Result '{}' does not appear to match any valid result format".format(result))
        return result


class Match():
    def __init__(self, winner='', loser='', result='', dbRecord=None):
        if dbRecord:
            self.winner = dbRecord['winner'].strip()
            self.loser = dbRecord['loser'].strip()
            self.result = _validate_result(dbRecord['result'].lower().strip())
        else:
            self.winner = winner.strip()
            self.loser = loser.strip()
            self.result = _validate_result(result.lower().strip())

    def __eq__(self, other):
        return self.winner == other.winner and self.loser == other.loser and self.result == other.result

    def __repr__(self):
        return "Winner: {}, Loser: {}, Result: {}".format(self.winner, self.loser, self.result)

    def insert(self, db):
        db.match_play.insert_one({'winner': self.winner,
                                  'loser': self.loser,
                                  'result': self.result})