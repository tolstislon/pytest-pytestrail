from .pytestrail_plugin import PyTestRail


def pytest_addoption(parser):
    parser.addoption('--pytestrail', action='store_true', help='Запуск интеграции с TestRail')
    parser.addoption('--tr-url', action='store', default=None, help='Адрес сервера TestRail')
    parser.addoption('--tr-email', action='store', default=None, help='Email акаунта в TestRail')
    parser.addoption('--tr-password', action='store', default=None, help='Пароль акаунта в TestRail')
    parser.addoption('--tr-test-run', action='store', default=None, help='ID test run')
    parser.addoption('--tr-no-decorator-skip', action='store', default=False, help='Скипать тесты без декоратора')

    parser.addini('pytestrail', help='Запуск интеграции с TestRail', type="bool", default=None)
    parser.addini('pytestrail-url', help='Адрес сервера TestRail', default=None)
    parser.addini('pytestrail-email', help='Email акаунта в TestRail', default=None)
    parser.addini('pytestrail-password', help='Пароль акаунта в TestRail', default=None)
    parser.addini('pytestrail-test-run', help='ID test run', default=None)
    parser.addini('pytestrail-no-decorator-skip', help='Скипать тесты без декоратора', default=False, type="bool")


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
