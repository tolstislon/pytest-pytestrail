from .pytestrail_plugin import PyTestRail


def pytest_addoption(parser):
    parser.addoption('--pytestrail', action='store_true', help='Enable plugin')
    parser.addoption('--tr-url', action='store', default=None, help='TestRail address')
    parser.addoption('--tr-email', action='store', default=None, help='Email for the account on the TestRail')
    parser.addoption('--tr-password', action='store', default=None, help='Password for the account on the TestRail')
    parser.addoption('--tr-test-run', action='store', default=None, help='ID testrun')
    parser.addoption('--tr-no-decorator-skip', action='store_true', help='Skip tests without decorator')

    parser.addini('pytestrail', help='Enable plugin', type="bool", default=None)
    parser.addini('pytestrail-url', help='TestRail address', default=None)
    parser.addini('pytestrail-email', help='Email for the account on the TestRail', default=None)
    parser.addini('pytestrail-password', help='Password for the account on the TestRail', default=None)
    parser.addini('pytestrail-test-run', help='ID testrun', default=None)
    parser.addini('pytestrail-no-decorator-skip', help='Skip tests without decorator', default=False, type="bool")


def pytest_configure(config):
    if config.getoption('--pytestrail') or config.getini('pytestrail'):
        config.pluginmanager.register(
            PyTestRail(
                url=config.getoption('--tr-url') or config.getini('pytestrail-url'),
                email=config.getoption('--tr-email') or config.getini('pytestrail-email'),
                password=config.getoption('--tr-password') or config.getini('pytestrail-password'),
                test_run=config.getoption('--tr-test-run') or config.getini('pytestrail-test-run')
            ),
            name="pytest-pytestrail-instance"
        )
