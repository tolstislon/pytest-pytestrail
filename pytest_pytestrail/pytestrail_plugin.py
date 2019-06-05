import itertools
import re
import threading
from queue import Queue

import pytest
from testrail_api import TestRailAPI

from . import _constants as constants
from ._exception import MissingRequiredParameter

REPORTER_QUEUE = None


def case_ids(item):
    return [int(re.search('(?P<id>[0-9]+$)', test_run_id).groupdict().get('id')) for test_run_id in
            [a for a in itertools.chain(*[i.args for i in item.iter_markers(constants.PYTESTRAIL_MARK)])]]


class Report:

    def __init__(self, ids, status, comment, elapsed):
        self.ids = ids
        self.status = status
        self.comment = self.pars_comment(comment)
        self.elapsed = elapsed

    @staticmethod
    def pars_comment(comment):
        if comment is None:
            return ''
        data = comment.__str__().split('\n')
        return '\n'.join([f'\t{line}' for line in data])


def reporter(api, test_run):
    while True:
        data = REPORTER_QUEUE.get()
        if isinstance(data, Report):
            for test_id in data.ids:
                request = {
                    'run_id': test_run,
                    'case_id': test_id,
                    'status_id': constants.STATUS[data.status],
                    'comment': data.comment,
                    'elapsed': f'{round(data.elapsed) or 1}s'
                }
                try:
                    api.results.add_result_for_case(**request)
                except Exception:
                    pass
        else:
            break


class PyTestRail:
    api: TestRailAPI
    case_ids: list

    def __init__(self, config):
        self.url: str = config.getoption('--tr-url') or config.getini('pytestrail-url')
        self.email: str = config.getoption('--tr-email') or config.getini('pytestrail-email')
        self.password: str = config.getoption('--tr-password') or config.getini('pytestrail-password')
        self.test_run = config.getoption('--tr-test-run') or config.getini('pytestrail-test-run')
        self.report = config.getoption('--tr-report') or config.getini('pytestrail-report')
        self.no_decorator_skip = config.getoption('--tr-no-decorator-skip') or config.getini(
            'pytestrail-no-decorator-skip')
        self.reporter = None

    def pytest_report_header(self):
        if self.url is None:
            raise MissingRequiredParameter('url')

        if self.email is None:
            raise MissingRequiredParameter('email')

        if self.password is None:
            raise MissingRequiredParameter('password')

        self.api = TestRailAPI(self.url, self.email, self.password)

        if self.test_run is None:
            raise MissingRequiredParameter('test-run')

        response = self.api.tests.get_tests(self.test_run)
        self.case_ids = [i['case_id'] for i in response]

        # create reporting
        if self.report:
            global REPORTER_QUEUE
            REPORTER_QUEUE = Queue()
            self.reporter = threading.Thread(target=reporter, args=(self.api, self.test_run))
            self.reporter.start()

        return f'PyTestRail {constants.__version__}: ON'

    @pytest.hookimpl(trylast=True)
    def pytest_collection_modifyitems(self, items, config):
        selected_items = []
        deselected_items = []

        for item in items:
            ids = case_ids(item)
            if not set(ids) & set(self.case_ids):
                if self.no_decorator_skip:
                    deselected_items.append(item)
                else:
                    selected_items.append(item)
            else:
                selected_items.append(item)

        config.hook.pytest_deselected(items=deselected_items)
        items[:] = selected_items

    @pytest.hookimpl(tryfirst=True, hookwrapper=True)
    def pytest_runtest_makereport(self, item):
        outcome = yield
        rep = outcome.get_result()

        if self.report:
            ids = case_ids(item)
            if rep.when == 'call' and ids:
                REPORTER_QUEUE.put(
                    Report(ids, rep.outcome, rep.longrepr, rep.duration)
                )
            elif rep.when in ('setup', 'teardown') and ids and rep.outcome != 'passed':
                REPORTER_QUEUE.put(
                    Report(ids, rep.outcome, rep.longrepr, rep.duration)
                )

    def pytest_sessionfinish(self):
        if self.report:
            self.stopped_report()

    def stopped_report(self):
        REPORTER_QUEUE.put('stop')
        print('\nCompleting Report Upload ...')
        self.reporter.join()
