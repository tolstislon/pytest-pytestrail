from typing import Any, Iterable, Iterator, Optional, TypeVar

import pytest

__all__ = ["case", "steps_case", "param", "params"]

ParameterSet = TypeVar("ParameterSet")


def case(case_id: str):
    return pytest.mark.pytestrail(case_id)


class steps_case:
    def __init__(self, case_id: str):
        self._case_id = case_id

    def step(self, step: int):
        return pytest.mark.pytestrail_case(self._case_id, step=step)


def param(value: Any, case_id: str, step: Optional[int] = None) -> ParameterSet:
    return pytest.param(
        value, marks=case(case_id) if step is None else steps_case(case_id).step(step)
    )


def params(case_id: str, parametrize: Iterable) -> Iterator[ParameterSet]:
    return (param(value, case_id, step) for step, value in enumerate(parametrize, 1))
