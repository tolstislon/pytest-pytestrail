from .pytestrail_plugin import PyTestRail
from ._constants import PYTESTRAIL_MARK, PYTESTRAIL_CASE_MARK


def pytest_addoption(parser):
    group = parser.getgroup('TestRail')
    group.addoption('--pytestrail', action='store_true', help='Enable plugin')
    group.addoption('--tr-url', action='store', default=None, help='TestRail address')
    group.addoption('--tr-email', action='store', default=None, help='Email for the account on the TestRail')
    group.addoption('--tr-password', action='store', default=None, help='Password for the account on the TestRail')
    group.addoption('--tr-test-run', action='store', default=None, help='ID testrun')
    group.addoption('--tr-no-decorator-skip', action='store_true', help='Skip tests without decorator', default=False)
    group.addoption('--tr-report', action='store_true', help='Enable report', default=False)

    parser.addini('pytestrail', help='Enable plugin', type="bool", default=None)
    parser.addini('pytestrail-url', help='TestRail address', default=None)
    parser.addini('pytestrail-email', help='Email for the account on the TestRail', default=None)
    parser.addini('pytestrail-password', help='Password for the account on the TestRail', default=None)
    parser.addini('pytestrail-test-run', help='ID testrun', default=None)
    parser.addini('pytestrail-no-decorator-skip', help='Skip tests without decorator', default=False, type="bool")
    parser.addini('pytestrail-report', help='Enable report', default=False, type="bool")


def pytest_configure(config):
    config.addinivalue_line("markers", f"{PYTESTRAIL_MARK}(*args): Mark test")
    config.addinivalue_line("markers", f"{PYTESTRAIL_CASE_MARK}(case_id, step): Mark test")
    if config.getoption('--pytestrail') or config.getini('pytestrail'):
        config.pluginmanager.register(PyTestRail(config), name="pytest-pytestrail-instance")
