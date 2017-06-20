class ValidationException(Exception):
    """Used to report failures to validate an input format"""

class IncompleteException(Exception):
    """Used to report when an import is being attempted to run against an unfinshed match,
    tournament, or event."""