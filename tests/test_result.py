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


def test_can_chain_successes() -> None:
    def _multiply(value: int) -> Result[int, RandomError]:
        return Success(value * value)

    assert Success(2).chain(_multiply) == Success(4)
    assert Success(2).chain(_multiply).chain(_multiply) == Success(16)


def test_can_chain_success_with_value() -> None:
    assert Result.with_value(1).chain(lambda a: Success(a + a)) == Success(2)


def test_chain_halts_with_inner_functions() -> None:
    def _error(value: int) -> Result:
        return Error(RandomError())

    def _multiply(value: int) -> Result:
        return Success(value * value)

    assert Success(2).chain(_multiply).chain(_error).chain(_multiply) == Error(
        RandomError()
    )
    assert Success(2).chain(_error).chain(_multiply) == Error(RandomError())


def test_chain_halts_with_error_at_start() -> None:
    def _add(value: int) -> Result[int, RandomError]:
        return value + value

    assert Result.with_error(RandomError()).chain(_add).chain(_add) == Error(
        RandomError()
    )
