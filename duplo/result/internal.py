from typing import Generic, TypeVar


class ResultError(Exception):
    def __init__(self, result: "_ResultT") -> None:
        self.result = result
        Exception.__init__(self)

    def __eq__(self, error: object) -> bool:
        return isinstance(error, type(self))


ErrT = TypeVar("ErrT", bound=ResultError)


A = TypeVar("A", covariant=True)
B = TypeVar("B")

E = TypeVar("E", covariant=True)
E_ = TypeVar("E_")


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

    def __eq__(self, _result: object) -> bool:
        raise NotImplementedError()

    def __ne__(self, _result: object) -> bool:
        raise NotImplementedError()

    def __str__(self) -> str:
        raise NotImplementedError()

    def __repr__(self) -> str:
        raise NotImplementedError()
