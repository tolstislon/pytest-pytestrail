from .pytestrail_plugin import PyTestRail
from ._constants import PYTESTRAIL_MARK, PYTESTRAIL_CASE_MARK


def pytest_addoption(parser):
    group = parser.getgroup('TestRail')

    _help = 'Enable plugin'
    group.addoption('--pytestrail', action='store_true', help=_help)
    parser.addini('pytestrail', help=_help, type="bool", default=None)

    _help = 'TestRail address'
    group.addoption('--tr-url', action='store', default=None, help=_help)
    parser.addini('pytestrail-url', help=_help, default=None)

    _help = 'Email for the account on the TestRail'
    group.addoption('--tr-email', action='store', default=None, help=_help)
    parser.addini('pytestrail-email', help=_help, default=None)

    _help = 'Password for the account on the TestRail'
    group.addoption('--tr-password', action='store', default=None, help=_help)
    parser.addini('pytestrail-password', help=_help, default=None)

    _help = 'ID testrun'
    group.addoption('--tr-test-run', action='store', default=None, help=_help)
    parser.addini('pytestrail-test-run', help=_help, default=None)

    _help = 'Skip tests without decorator'
    group.addoption('--tr-no-decorator-skip', action='store_true', help=_help, default=False)
    parser.addini('pytestrail-no-decorator-skip', help=_help, default=False, type="bool")

    _help = 'Enable report'
    group.addoption('--tr-report', action='store_true', help=_help, default=False)
    parser.addini('pytestrail-report', help=_help, default=False, type="bool")


def pytest_configure(config):
    config.addinivalue_line("markers", f"{PYTESTRAIL_MARK}(*args): Mark test")
    config.addinivalue_line("markers", f"{PYTESTRAIL_CASE_MARK}(case_id, step): Mark test")
    if config.getoption('--pytestrail') or config.getini('pytestrail'):
        config.pluginmanager.register(PyTestRail(config), name="pytest-pytestrail-instance")
