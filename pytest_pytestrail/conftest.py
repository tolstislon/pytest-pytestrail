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
    group.addoption('--tr-test-run', action='store', default=None, help=_help, type=int)
    parser.addini('pytestrail-test-run', help=_help, default=None)

    _help = 'Skip tests without decorator'
    group.addoption('--tr-no-decorator-skip', action='store_true', help=_help, default=False)
    parser.addini('pytestrail-no-decorator-skip', help=_help, default=False, type="bool")

    _help = 'Enable report'
    group.addoption('--tr-report', action='store_true', help=_help, default=False)
    parser.addini('pytestrail-report', help=_help, default=False, type="bool")

    _help = 'Do not check for valid SSL certificate on TestRail host'
    group.addoption('--tr-no-ssl-check', action='store_true', help=_help, default=False)
    parser.addini('pytestrail-no-ssl-check', help=_help, default=False, type="bool")

    _help = 'ID of the project'
    group.addoption('--tr-project-id', action='store', default=None, help=_help, type=int)
    parser.addini('pytestrail-project-id', help=_help, default=None)

    _help = 'ID of the test suite'
    group.addoption('--tr-suite-id', action='store', default=None, help=_help, type=int)
    parser.addini('pytestrail-suite-id', help=_help, default=None)

    _help = 'Name given to testrun, that appears in TestRail'
    group.addoption('--tr-testrun-name', action='store', default=None, help=_help)
    parser.addini('pytestrail-testrun-name', help=_help, default='Auto generated {datetime}')

    _help = 'Date format (default: %Y-%m-%d %H:%M:%S)'
    group.addoption('--tr-date-format', action='store', default=None, help=_help)
    parser.addini('pytestrail-date-format', help=_help, default='%Y-%m-%d %H:%M:%S')

    _help = 'Use local time zone (Default: UTC)'
    group.addoption('--tr-tz-local', action='store_true', help=_help, default=False)
    parser.addini('pytestrail-tz-local', help=_help, default=False, type="bool")

    _help = 'Close test run on completion'
    group.addoption('--tr-close-on-complete', action='store_true', help=_help, default=False)
    parser.addini('pytestrail-close-on-complete', help=_help, default=False, type="bool")

    _help = 'Set test tun milestone'
    group.addoption('--tr-milestone-id', action='store', default=None, help=_help, type=int)
    parser.addini('pytestrail-milestone-id', help=_help, default=None)

    _help = 'Description given to testrun, that appears in TestRail'
    group.addoption('--tr-testrun-description', action='store', default=None, help=_help)
    parser.addini('pytestrail-testrun-description', help=_help,
                  default='Auto generated {datetime} PyTestRail {__version__}')


def pytest_configure(config):
    config.addinivalue_line("markers", f"{PYTESTRAIL_MARK}(*args): Mark test")
    config.addinivalue_line("markers", f"{PYTESTRAIL_CASE_MARK}(case_id, step): Mark test")
    if config.getoption('--pytestrail') or config.getini('pytestrail'):
        config.pluginmanager.register(PyTestRail(config), name="pytest-pytestrail-instance")
