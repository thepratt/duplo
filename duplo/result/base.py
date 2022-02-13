from typing import ClassVar, Type
from .exceptions import InvalidResultStateError
from .internal import _ResultT, E, A, B, E_
from typing import Callable, NoReturn, Union, cast, final


class Result(_ResultT[E, A]):
    __slots__ = ()

    _inner_value: Union[E, A]

    _success_type: ClassVar[Type["Success"]]
    _error_type: ClassVar[Type["Error"]]

    def chain(
        self, next: Callable[[A], "Result[B, Union[E, E_]]"]
    ) -> "Result[B, Union[E, E_]]":
        if self.is_success():
            return next(self._inner_value)

        if self.is_error():
            return cast(Result[A, Union[E, E_]], self)

        raise InvalidResultStateError(self)

    @classmethod
    def with_error(self, error: E) -> "Result[E, A]":
        return Error(error)

    @classmethod
    def with_value(self, value: A) -> "Result[E, A]":
        return Success(value)

    @staticmethod
    def handle(
        result: "Result[E, A]",
        *,
        on_success: Callable[[A], B],
        on_error: Callable[[E], NoReturn],
    ) -> B:
        """
        Complete a chain of `Result`s, equivalent in understanding to `flatmap`

        on_success will transform the success-side (right) into the preferred,
        unwrapped value.
        on_error will handle on_error into the final type before throwing.
        """
        if result.is_success():
            value = result.unwrap()
            return on_success(value)

        if result.is_error():
            error = result.error()
            raise on_error(error)

        return NotImplementedError()


@final
class Success(Result[E, A]):
    __slots__ = ("_inner_value",)
    __match_args__ = ("_inner_value",)

    _inner_value: A

    def __init__(self, value: A) -> None:
        self._inner_value = value

    def is_error(self) -> bool:
        return False

    def is_success(self) -> bool:
        return True

    def unwrap(self) -> A:
        return self._inner_value

    def error(self) -> NoReturn:
        raise InvalidResultStateError(result=self)

    def __eq__(self, result: Result[E, A]) -> bool:
        if not isinstance(result, Result):
            return False

        if not result.is_success():
            return False

        return self._inner_value == result.unwrap()

    def __ne__(self, result: Result[E, A]) -> bool:
        return not self == result

    def __str__(self) -> str:
        return f"<Success: {self._inner_value!r}>"

    def __repr__(self) -> str:
        return str(self)


@final
class Error(Result[E, A]):
    __slots__ = ("_inner_value",)
    __match_args__ = ("_inner_value",)

    _inner_value: E

    def __init__(self, error: E) -> None:
        self._inner_value = error

    def is_error(self) -> bool:
        return True

    def is_success(self) -> bool:
        return False

    def unwrap(self) -> A:
        raise self._inner_value

    def error(self) -> E:
        return self._inner_value

    def __eq__(self, result: Result[E, A]) -> bool:
        if not isinstance(result, Result):
            return False

        if not result.is_error():
            return False

        return self.error().__class__ == result.error().__class__

    def __ne__(self, result: Result[E, A]) -> bool:
        return not self == result

    def __str__(self) -> str:
        return f"<Error: {self._inner_value.__class__}>"

    def __repr__(self) -> str:
        return str(self)
