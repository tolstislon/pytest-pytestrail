import itertools
import re

import colorama
import pytest
from testrail_api import TestRailAPI

from ._exception import MissingRequiredParameter

__version__ = '0.0.1a'

PYTESTRAIL_MARK = 'pytestrail'


class pytestrail:

    @staticmethod
    def case(*args):
        return pytest.mark.pytestrail(*args)


class PyTestRail:
    api: TestRailAPI
    case_ids: list

    def __init__(self, url, email, password, test_run):
        self.url = url
        self.email = email
        self.password = password
        self.test_run = test_run

    def pytest_report_header(self, config, startdir):
        if not self.url:
            raise MissingRequiredParameter('url')
        if not self.email:
            raise MissingRequiredParameter('email')
        if not self.password:
            raise MissingRequiredParameter('password')

        self.api = TestRailAPI(self.url, self.email, self.password)

        if not self.test_run:
            raise MissingRequiredParameter('test-run')

        response = self.api.tests.get_tests(self.test_run)
        self.case_ids = [i['case_id'] for i in response]

        colorama.init(autoreset=True)
        return f'PyTestRail {__version__}: {colorama.Fore.GREEN}ON{colorama.Fore.RESET}'

    @pytest.hookimpl(trylast=True)
    def pytest_collection_modifyitems(self, session, config, items):
        """"""
        for item in items:
            ids = [int(re.search('(?P<id>[0-9]+$)', test_id).groupdict().get('id')) for test_id in
                   [a for a in itertools.chain(*[i.args for i in item.iter_markers(PYTESTRAIL_MARK)])]]

            if ids:
                if not set(ids) & set(self.case_ids):
                    mark = pytest.mark.skip(f'Test absent in testrun {self.test_run}')
                    item.add_marker(mark)
            else:
                if config.getoption('--tr-no-decorator-skip') or config.getini('pytestrail-no-decorator-skip'):
                    mark = pytest.mark.skip(f'No {PYTESTRAIL_MARK} decorator')
                    item.add_marker(mark)
