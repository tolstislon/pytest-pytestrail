import re
from typing import Optional, Tuple

from . import _constants as cons


class Case:

    def __init__(self, case_id: int, step: Optional[int] = None):
        self.case_id = case_id
        self.step = step
        self.last = False

    @property
    def is_step(self) -> bool:
        return self.step is not None

    @property
    def is_last(self) -> bool:
        return self.last

    def __repr__(self):
        return f'<{self.__class__.__name__}(case_id:{self.case_id}, step: {self.step})>'


def get_case_id(data: tuple) -> Optional[int]:
    nums = [int(re.search('(?P<id>[0-9]+$)', test_id).groupdict().get('id')) for test_id in data]
    return nums[0] if nums else None


def case_markers(item) -> Tuple[bool, int]:
    for i in item.iter_markers(name=cons.PYTESTRAIL_MARK):
        num = get_case_id(i.args)
        if isinstance(num, int):
            setattr(item, 'pytestrail_case', Case(num))
            return True, num
    for i in item.iter_markers(name=cons.PYTESTRAIL_CASE_MARK):
        num = get_case_id(i.args)
        if isinstance(num, int):
            step = i.kwargs['step']
            setattr(item, 'pytestrail_case', Case(num, step))
            return True, num
    return False, -1
