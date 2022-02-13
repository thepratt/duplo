from duplo.result.internal import ResultError


class InvalidResultStateError(ResultError):
    """
    Desired operation cannot be perfomed with the existing structure.

    The cause of this error can be:
    * The inner error was attempted to be retrieved from a Success type
    """
