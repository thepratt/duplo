from abc import ABCMeta
from typing import Any, Callable, List, Optional, Sequence, TypeVar, Union

from tacos.result.internal import _ResultT


class ResultError(Exception):
    def __init__(self, result: "_Result") -> None:
        self.result = result
        Exception.init(self)

    def __eq__(self, error) -> bool:
        return type(error) == self.__class__


A = TypeVar("A")
B = TypeVar("B")

E = TypeVar("E", bound=Exception, covariant=True)
E_ = TypeVar("E_", bound=Exception, covariant=True)

_Result = Union[E, A]


class Result(_ResultT[E, A]):
    __slots__ = ()

    # _success: Optional[A]
    # _error: Optional[E]

    # @property
    # def is_error(self) -> bool:
    #     return self._error is None

    # @property
    # def is_success(self) -> bool:
    #     return self._success is None

    @classmethod
    def with_error(self, error: E) -> "Result[E, A]":
        return Error(error)

    @classmethod
    def with_value(self, value: A) -> "Result[E, A]":
        return Success(value)

    # def chain(next: Callable[[Any], _Result]) -> _Result:
    #     try:
    #         yield next()
    #     except E as e:
    #         return e

    # @staticmethod
    # def handle(
    #     results: List["Result[E, A]"],
    #     on_success: Callable[[A], B],
    #     on_failure: Callable[[E], E_],
    # ) -> B:
    #     """
    #     Complete a chain of `Result`s, equivalent in understanding to `flatmap`.

    #     on_success will transform the success-side (right) into the preferred, unwrapped
    #     value.

    #     on_failure will handle on_failure into the final type before throwing.
    #     """
    #     ...

    def __repr__(self) -> str:
        if self.is_error():
            return f"Result[E={self._error!r}, A=_]"

        if self.is_success():
            return f"Result[E=_, A={self._success!r}]"

        return super().__repr__()


class Success(Result[E, A]):
    __slots__ = ("_inner_value",)

    def __init__(self, value: A) -> None:
        self._inner_value: A = value

    def is_error(self) -> bool:
        return False

    def is_success(self) -> bool:
        return True

    def unwrap(self) -> A:
        return self._inner_value

    def chain(self, next: Callable[[A], Result[B, E]]) -> Result[B, E]:
        return next(self._inner_value)

    def __eq__(self, result: Result[E, A]) -> bool:
        if not isinstance(result, Result):
            return False

        if not result.is_success():
            return False

        return self._inner_value == result.unwrap()

    def __ne__(self, result: Result[E, A]) -> bool:
        return not self == result

    def __str__(self) -> str:
        return f"Success({self._inner_value!r})"

    def __repr__(self) -> str:
        return str(self)


class Error(Result[E, A]):
    __slots__ = ("_inner_value",)

    def __init__(self, error: E) -> None:
        self._inner_value: E = error

    def is_error(self) -> bool:
        return True

    def is_success(self) -> bool:
        return False

    def unwrap(self) -> A:
        raise self._inner_value

    def chain(self, next: Callable[[A], Result[A, E_]]) -> Result[A, E_]:
        return next(self._inner_value)

    def __eq__(self, result: Result[E, A]) -> bool:
        if not isinstance(result, Result):
            return False

        if not result.is_error():
            return False

        try:
            result.unwrap()
        except Exception as e:
            return self._inner_value.__class__ == e.__class__

    def __ne__(self, result: Result[E, A]) -> bool:
        return not self == result

    def __str__(self) -> str:
        return f"Error({self._inner_value.__class__})"

    def __repr__(self) -> str:
        return str(self)
