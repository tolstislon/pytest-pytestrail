import itertools
import re

import colorama
import pytest
from testrail_api import TestRailAPI

from . import _constants as constants
from ._exception import MissingRequiredParameter


class PytestrailMark:

    @staticmethod
    def case(*args):
        return pytest.mark.pytestrail(*args)


def testrail(*args):
    """Support lib pytest-testrail"""
    return PytestrailMark.case(*args)


def case_ids(item):
    return [int(re.search('(?P<id>[0-9]+$)', test_run_id).groupdict().get('id')) for test_run_id in
            [a for a in itertools.chain(*[i.args for i in item.iter_markers(constants.PYTESTRAIL_MARK)])]]


class PyTestRail:
    api: TestRailAPI
    case_ids: list

    def __init__(self):
        self.url = self.email = self.password = self.test_run = None

    def pytest_report_header(self, config, startdir):
        """"""
        self.url = config.getoption('--tr-url') or config.getini('pytestrail-url')
        if self.url is None:
            raise MissingRequiredParameter('url')

        self.email = config.getoption('--tr-email') or config.getini('pytestrail-email')
        if self.email is None:
            raise MissingRequiredParameter('email')

        self.password = config.getoption('--tr-password') or config.getini('pytestrail-password')
        if self.password is None:
            raise MissingRequiredParameter('password')

        self.api = TestRailAPI(self.url, self.email, self.password)

        self.test_run = config.getoption('--tr-test-run') or config.getini('pytestrail-test-run')
        if self.test_run is None:
            raise MissingRequiredParameter('test-run')

        response = self.api.tests.get_tests(self.test_run)
        self.case_ids = [i['case_id'] for i in response]

        colorama.init(autoreset=True)
        return f'PyTestRail {constants.__version__}: {colorama.Fore.GREEN}ON{colorama.Fore.RESET}'

    @pytest.hookimpl(trylast=True)
    def pytest_collection_modifyitems(self, session, config, items):
        """"""
        for item in items:
            ids = case_ids(item)

            if ids:
                if not set(ids) & set(self.case_ids):
                    item.add_marker(pytest.mark.skip(f'Test absent in testrun {self.test_run}'))
            else:
                if config.getoption('--tr-no-decorator-skip') or config.getini('pytestrail-no-decorator-skip'):
                    item.add_marker(pytest.mark.skip('Skip tests without decorator'))

    @pytest.hookimpl(tryfirst=True, hookwrapper=True)
    def pytest_runtest_makereport(self, item, call):
        """"""
        outcome = yield
        rep = outcome.get_result()

        ids = case_ids(item)
        if rep.when == 'call' and ids:
            self.set_result(
                ids,
                outcome.get_result().outcome,
                rep.longrepr,
                rep.duration
            )

    def set_result(self, ids, status, comment, elapsed):

        for test_id in ids:
            self.api.results.add_result_for_case(self.test_run, test_id,
                                                 status_id=constants.STATUS[status],
                                                 comment=comment.__str__() + f'\n\n\nelapsed: {elapsed}')
