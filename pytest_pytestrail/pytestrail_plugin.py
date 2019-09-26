from typing import Union

import pytest

from .__version__ import __version__
from ._case import case_markers
from ._config import Config
from ._sender import Sender, FakeSender


class PyTestRail:
    case_ids: list
    reporter: Union[Sender, FakeSender]

    def __init__(self, conf):
        self._config = Config(conf)
        self.reporter = FakeSender()

    def _selection_item(self, mark, case_id) -> bool:
        # TODO Implement selection
        if not mark or case_id not in self.case_ids:
            return False
        return True

    @staticmethod
    def _sorted_items(items) -> None:
        h = {}
        for item in items:
            case = getattr(item, 'pytestrail_case', None)
            if case is not None and case.is_step:
                case_items = h.setdefault(case.case_id, [])
                case_items.append(item)
        for case_items in h.values():
            if len(case_items) > 1:
                case_items.sort(key=lambda x: x.pytestrail_case.step)
                for count, item in enumerate(case_items):
                    if count != 0:
                        items.pop(items.index(item))
                        start = items.index(case_items[0])
                        items.insert(start + count, item)
                        if count == len(case_items) - 1:
                            setattr(item.pytestrail_case, 'last', True)
            else:
                setattr(case_items[0].pytestrail_case, 'last', True)

    def pytest_report_header(self):
        self.case_ids = self._config.get_case_ids()

        # create reporting
        if self._config.report:
            self.reporter = Sender(api=self._config.api, run_id=self._config.get_test_run())
            self.reporter.start()

        return f'PyTestRail {__version__}: ON'

    @pytest.hookimpl(trylast=True)
    def pytest_collection_modifyitems(self, items, config):
        selected_items = []

        deselected_items = []
        for item in items:
            mark, case_id = case_markers(item)
            if self._selection_item(mark, case_id):
                selected_items.append(item)
            else:
                deselected_items.append(item)
        self._sorted_items(selected_items)
        config.hook.pytest_deselected(items=deselected_items)
        items[:] = selected_items

    @pytest.hookimpl(tryfirst=True, hookwrapper=True)
    def pytest_runtest_makereport(self, item):
        outcome = yield
        rep = outcome.get_result()

        ids = hasattr(item, 'pytestrail_case')
        if rep.when == 'call' and ids:
            self.reporter.send(item.pytestrail_case, rep)
        elif rep.when in ('setup', 'teardown') and ids and rep.outcome != 'passed':
            self.reporter.send(item.pytestrail_case, rep)

    def pytest_sessionfinish(self):
        self.reporter.stop()
        self.reporter.join()
