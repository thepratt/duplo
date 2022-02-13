from typing import Callable, Generic, TypeVar


class ResultError(Exception):
    def __init__(self, result: "_ResultT") -> None:
        self.result = result
        Exception.__init__(self)

    def __eq__(self, error) -> bool:
        return isinstance(error, self)


A = TypeVar("A")
B = TypeVar("B")

E = TypeVar("E", bound=Exception, covariant=True)
E_ = TypeVar("E_", bound=Exception, covariant=True)


class _ResultT(Generic[E, A]):
    __slots__ = ()

    def is_error(self) -> bool:
        raise NotImplementedError()

    def is_success(self) -> bool:
        raise NotImplementedError()

    def unwrap(self) -> A:
        raise NotImplementedError()

    def error(self) -> E:
        raise NotImplementedError()

    def chain(self, next: Callable[[A], "_ResultT[B, E]"]) -> "_ResultT[B, E]":
        raise NotImplementedError()

    def __eq__(self, _result: "_ResultT[E, A]") -> bool:
        raise NotImplementedError()

    def __ne__(self, _result: "_ResultT[E, A]") -> bool:
        raise NotImplementedError()

    def __str__(self) -> str:
        raise NotImplementedError()

    def __repr__(self) -> str:
        raise NotImplementedError()
