import warnings
from typing import Any, Optional, Iterable, Generator

import pytest

__all__ = [
    'case',
    'steps_case',
    'param',
    'params'
]


def case(case_id: str, *args):
    if args:
        warnings.warn('case takes only one argument', DeprecationWarning)
    return pytest.mark.pytestrail(case_id)


class steps_case:

    def __init__(self, case_id: str):
        self._case_id = case_id

    def step(self, step: int):
        return pytest.mark.pytestrail_case(self._case_id, step=step)


def param(value: Any, case_id: str, step: Optional[int] = None):
    return pytest.param(value, marks=case(case_id) if step is None else steps_case(case_id).step(step))


def params(case_id: str, parametrize: Iterable) -> Generator:
    return (param(value, case_id, step) for step, value in enumerate(parametrize, 1))
