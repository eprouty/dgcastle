from dgcastle.exceptions import ValidationException

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
        elif '-' in result:
            # Challonge results are output in the format X-Y... need to normalize that
            try:
                p1_score, p2_score = result.split('-')
                if p1_score == '0' or p2_score == '0':
                    # This is an Xup result
                    X = int(p1_score) + int(p2_score)
                    return _validate_result('{}up'.format(X))
                else:
                    # Should be a X&Y result (no ties in tournament brackets)
                    x, y = [p1_score, p2_score] if p1_score > p2_score else [p2_score, p1_score]
                    return _validate_result('{}&{}'.format(x, y))
            except ValueError:
                raise ValidationException("Challonge result '{}' failed validation".format(result))

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
        elif ('&' in result) != ('+' in result):
            sep = '&' if '&' in result else '+'
            tmp = result.split(sep)
            if len(tmp) != 2:
                # We've got extra info here
                raise ValidationException("Result '{}' not in the format 'X{}Y'".format(result, sep))
            try:
                X = int(tmp[0])
                Y = int(tmp[1])
                if X > 1  and X > Y >= 1 and X - Y <= 2:
                    # we're good here
                    pass
                else:
                    raise ValidationException("Result '{}' is not a valid score. Given the format 'X{}Y' must have X > 1 and X > Y >= 1".format(result, sep))
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
            self.winner = winner.name.strip()
            self.loser = loser.name.strip()
            self.result = _validate_result(result.lower().strip())

    def __eq__(self, other):
        return self.winner == other.winner and self.loser == other.loser and self.result == other.result

    def __repr__(self):
        return "Winner: {}, Loser: {}, Result: {}".format(self.winner, self.loser, self.result)

    def insert(self, db):
        db.match_play.insert_one({'winner': self.winner,
                                  'loser': self.loser,
                                  'result': self.result})