from typing import Union, get_args, get_type_hints
import pytest
from duplo.result import Result, Success, Error
from duplo.result.exceptions import InvalidResultStateError


class RandomError(Exception):
    pass


class OtherError(Exception):
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


def test_success_can_be_unwrapped() -> None:
    assert Success(1).unwrap() == 1
    assert Success(None).unwrap() is None


def test_success_does_not_have_inner_error() -> None:
    with pytest.raises(InvalidResultStateError):
        Success(1).error()


def test_error_can_introspect_inner_error() -> None:
    assert isinstance(Error(RandomError()).error(), RandomError)


def test_error_cannot_be_unwrapped() -> None:
    with pytest.raises(RandomError):
        Error(RandomError()).unwrap()


def test_can_chain_successes_of_different_types() -> None:
    def _multiply(value: int) -> Result[int, RandomError]:
        return Success(value * value)

    def _to_string(value: int) -> Result[str, RandomError]:
        return Success(str(value))

    assert Success(2).chain(_multiply) == Success(4)
    assert Success(2).chain(_multiply).chain(_to_string) == Success("4")


def test_can_chain_success_with_value() -> None:
    assert Result.with_value(1).chain(lambda a: Success(a + a)) == Success(2)


def test_chain_halts_with_inner_functions() -> None:
    def _error(_value: int) -> Result[int, RandomError]:
        return Error(RandomError())

    def _multiply(value: int) -> Result[int, OtherError]:
        return Success(value * value)

    assert Success(2).chain(_multiply).chain(_error).chain(_multiply) == Error(
        RandomError()
    )
    assert Success(2).chain(_error).chain(_multiply) == Error(RandomError())


def test_chained_errors_compose_in_union() -> None:
    def step_1() -> Result[int, RandomError]:
        return Success(1)

    def step_2(value: int) -> Result[str, OtherError]:
        return Success(str(value))

    def composed() -> Result[str, Union[RandomError, OtherError]]:
        return step_1().chain(step_2)

    assert get_args(get_type_hints(step_1)["return"]) == (int, RandomError)
    assert get_args(get_type_hints(step_2)["return"]) == (str, OtherError)
    assert get_args(get_type_hints(composed)["return"]) == (
        str,
        Union[RandomError, OtherError],
    )


# TODO: types should be collated as a `Union[Error, ...]`
def test_chain_halts_with_error_at_start() -> None:
    def _add(value: int) -> Result[int, OtherError]:
        return value + value

    res = Result.with_error(RandomError()).chain(_add).chain(_add)
    assert res == Error(RandomError())


def test_can_handle_single_result() -> None:
    def _mk_handle(result: Result[int, RandomError]) -> int:
        return Result.handle(
            result,
            on_success=lambda a: a + a,
            on_error=lambda e: OtherError() if isinstance(e, RandomError) else e,
        )

    assert _mk_handle(Success(2)) == Success(4).unwrap()

    assert (
        _mk_handle(
            Success(2).chain(lambda a: Success(a * a)).chain(lambda a: Success(a * 0))
        )
        == Success(0).unwrap()
    )

    with pytest.raises(OtherError):
        _mk_handle(Error(RandomError()))
