from tacos.result import Result, Success, Error


class RandomError(Exception):
    pass


def test_success_can_be_compared() -> None:
    assert Success(1) == Success(1)
    assert Success(None) != Success("abc")


def test_error_can_be_compared() -> None:
    assert Error(Exception()) == Error(Exception())
    assert Error(RandomError()) == Error(RandomError())
    assert Error(RandomError()) != Error(Exception())


def test_can_mark_success_as_success() -> None:
    assert Success(1).is_success() is True


def test_cannot_mark_error_as_success() -> None:
    assert Error(Exception()).is_success() is False


def test_can_mark_error_as_error() -> None:
    assert Error(Exception()).is_error() is True


def test_cannot_mark_success_as_error() -> None:
    assert Success(1).is_error() is False


def test_result_with_error_same_as_error() -> None:
    assert Result.with_error(RandomError()) == Error(RandomError())
    assert Result.with_error(Exception()) != Error(RandomError())


def test_result_with_value_same_as_success() -> None:
    assert Result.with_value(1) == Success(1)
    assert Result.with_value(None) != Success(2)
