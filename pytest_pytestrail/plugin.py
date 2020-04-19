from typing import Dict, List, Union

import pytest

from . import __version__
from ._case import Case, case_markers
from ._config import Config
from ._constants import PYTESTRAIL_CASE_MARK, PYTESTRAIL_MARK
from ._sender import FakeSender, Sender


def pytest_addoption(parser):
    group = parser.getgroup("TestRail")

    _help = "Enable plugin"
    group.addoption("--pytestrail", action="store_true", help=_help)
    parser.addini("pytestrail", help=_help, type="bool", default=None)

    _help = "TestRail address"
    group.addoption("--tr-url", action="store", default=None, help=_help)
    parser.addini("pytestrail-url", help=_help, default=None)

    _help = "Email for the account on the TestRail"
    group.addoption("--tr-email", action="store", default=None, help=_help)
    parser.addini("pytestrail-email", help=_help, default=None)

    _help = "Password for the account on the TestRail"
    group.addoption("--tr-password", action="store", default=None, help=_help)
    parser.addini("pytestrail-password", help=_help, default=None)

    _help = "ID testrun"
    group.addoption("--tr-test-run", action="store", default=None, help=_help, type=int)
    parser.addini("pytestrail-test-run", help=_help, default=None)

    _help = "Skip tests without decorator"
    group.addoption(
        "--tr-no-decorator-skip", action="store_true", help=_help, default=False
    )
    parser.addini(
        "pytestrail-no-decorator-skip", help=_help, default=False, type="bool"
    )

    _help = "Enable report"
    group.addoption("--tr-report", action="store_true", help=_help, default=False)
    parser.addini("pytestrail-report", help=_help, default=False, type="bool")

    _help = "Do not check for valid SSL certificate on TestRail host"
    group.addoption("--tr-no-ssl-check", action="store_true", help=_help, default=False)
    parser.addini("pytestrail-no-ssl-check", help=_help, default=False, type="bool")

    _help = "ID of the project"
    group.addoption(
        "--tr-project-id", action="store", default=None, help=_help, type=int
    )
    parser.addini("pytestrail-project-id", help=_help, default=None)

    _help = "ID of the test suite"
    group.addoption("--tr-suite-id", action="store", default=None, help=_help, type=int)
    parser.addini("pytestrail-suite-id", help=_help, default=None)

    _help = "Name given to testrun, that appears in TestRail"
    group.addoption("--tr-testrun-name", action="store", default=None, help=_help)
    parser.addini(
        "pytestrail-testrun-name", help=_help, default="Auto generated {datetime}"
    )

    _help = "Date format (default: %Y-%m-%d %H:%M:%S)"
    group.addoption("--tr-date-format", action="store", default=None, help=_help)
    parser.addini("pytestrail-date-format", help=_help, default="%Y-%m-%d %H:%M:%S")

    _help = "Use local time zone (Default: UTC)"
    group.addoption("--tr-tz-local", action="store_true", help=_help, default=False)
    parser.addini("pytestrail-tz-local", help=_help, default=False, type="bool")

    _help = "Close test run on completion"
    group.addoption(
        "--tr-close-on-complete", action="store_true", help=_help, default=False
    )
    parser.addini(
        "pytestrail-close-on-complete", help=_help, default=False, type="bool"
    )

    _help = "Set test tun milestone"
    group.addoption(
        "--tr-milestone-id", action="store", default=None, help=_help, type=int
    )
    parser.addini("pytestrail-milestone-id", help=_help, default=None)

    _help = "Description given to testrun, that appears in TestRail"
    group.addoption(
        "--tr-testrun-description", action="store", default=None, help=_help
    )
    parser.addini(
        "pytestrail-testrun-description",
        help=_help,
        default="Auto generated {datetime} PyTestRail {__version__}",
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "{}(*args): Mark test".format(PYTESTRAIL_MARK))
    config.addinivalue_line(
        "markers", "{}(case_id, step): Mark test".format(PYTESTRAIL_CASE_MARK)
    )
    if config.getoption("--pytestrail") or config.getini("pytestrail"):
        pytestrail = PyTestRail(config)
        config._pytestrail = pytestrail
        config.pluginmanager.register(pytestrail)


class _Function(pytest.Function):
    def pytestrail_case(self) -> Case:
        pass


class PyTestRail:
    def __init__(self, conf):
        self._config = Config(conf)
        self.reporter = FakeSender()  # type: Union[Sender, FakeSender]
        self.case_ids = []  # type: List[int]

    def _selection_item(self, mark, case_id: int) -> bool:
        # TODO Implement selection
        if not mark or case_id not in self.case_ids:
            return False
        return True

    @staticmethod
    def _sorted_items(items: List[pytest.Function]) -> None:
        step_cases = {}  # type: Dict[int, list]
        for item in items:
            case = getattr(item, "pytestrail_case", None)
            if case is not None and case.is_step:
                case_items = step_cases.setdefault(case.case_id, [])
                case_items.append(item)
        for case_items in step_cases.values():
            if len(case_items) > 1:
                case_items.sort(key=lambda x: x.pytestrail_case.step)
                for count, item in enumerate(case_items):
                    if count != 0:
                        items.pop(items.index(item))
                        start = items.index(case_items[0])
                        items.insert(start + count, item)
                        if count == len(case_items) - 1:
                            setattr(item.pytestrail_case, "last", True)
            else:
                setattr(case_items[0].pytestrail_case, "last", True)

    def pytest_report_header(self) -> str:
        self.case_ids = self._config.get_case_ids(self._config.test_run)

        # create reporting
        if self._config.report:
            self.reporter = Sender(
                api=self._config.api, run_id=self._config.get_test_run()
            )
            self.reporter.start()

        return "PyTestRail {}: ON".format(__version__)

    @pytest.hookimpl(trylast=True)
    def pytest_collection_modifyitems(
        self, items: List[pytest.Function], config
    ) -> None:
        selected_items = []  # type: List[pytest.Function]
        deselected_items = []  # type: List[pytest.Function]

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
    def pytest_runtest_makereport(
        self, item: Union[pytest.Function, _Function]
    ) -> None:
        outcome = yield
        rep = outcome.get_result()

        ids = hasattr(item, "pytestrail_case")
        if rep.when == "call" and ids:
            self.reporter.send(item.pytestrail_case, rep)
        elif rep.when in ("setup", "teardown") and ids and rep.outcome != "passed":
            self.reporter.send(item.pytestrail_case, rep)

    def pytest_sessionfinish(self):
        self.reporter.stop()
        self.reporter.join()
        self._config.close()
