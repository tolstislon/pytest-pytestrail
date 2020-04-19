from datetime import datetime
from functools import lru_cache
from typing import List

import pytest
from testrail_api import TestRailAPI

from . import __version__


class _Dict(dict):
    def __missing__(self, key):
        return "{%s}" % key


class Config:
    def __init__(self, conf) -> None:
        self.url = conf.getoption("--tr-url") or conf.getini("pytestrail-url")
        self.email = conf.getoption("--tr-email") or conf.getini("pytestrail-email")
        self.password = conf.getoption("--tr-password") or conf.getini(
            "pytestrail-password"
        )
        self.test_run = conf.getoption("--tr-test-run") or conf.getini(
            "pytestrail-test-run"
        )
        self.report = conf.getoption("--tr-report") or conf.getini("pytestrail-report")
        self.no_decorator_skip = conf.getoption(
            "--tr-no-decorator-skip"
        ) or conf.getini("pytestrail-no-decorator-skip")
        self.ssl_check = conf.getoption("--tr-no-ssl-check") or conf.getini(
            "pytestrail-no-ssl-check"
        )
        self.project_id = conf.getoption("--tr-project-id") or conf.getini(
            "pytestrail-project-id"
        )
        self.suite_id = conf.getoption("--tr-suite-id") or conf.getini(
            "pytestrail-suite-id"
        )
        self.testrun_name = conf.getoption("--tr-testrun-name") or conf.getini(
            "pytestrail-testrun-name"
        )
        self.date_format = conf.getoption("--tr-date-format") or conf.getini(
            "pytestrail-date-format"
        )
        self.close_on_complete = conf.getoption(
            "--tr-close-on-complete"
        ) or conf.getini("pytestrail-close-on-complete")
        self.milestone_id = conf.getoption("--tr-milestone-id") or conf.getini(
            "pytestrail-milestone-id"
        )
        self.tz_local = conf.getoption("--tr-tz-local") or conf.getini(
            "pytestrail-tz-local"
        )
        self.testrun_description = conf.getoption(
            "--tr-testrun-description"
        ) or conf.getini("pytestrail-testrun-description")

        self.__date_time = datetime.now() if self.tz_local else datetime.utcnow()
        self._conf = conf
        self.api = TestRailAPI(
            self.url, self.email, self.password, verify=not self.ssl_check
        )
        self.work()

    def work(self) -> None:
        if self.project_id:
            val = {
                "project_id": self.project_id,
                "name": self._format_string(self.testrun_name),
                "description": self._format_string(self.testrun_description),
            }
            if self.suite_id:
                val["suite_id"] = self.suite_id
            if self.milestone_id:
                val["milestone_id"] = self.milestone_id
            if self.test_run:
                val["case_ids"] = self.get_case_ids(self.test_run)
                val["include_all"] = False
            else:
                val["include_all"] = True
            response = self.api.runs.add_run(**val)
            self.test_run = response["id"]
        elif not self.test_run:
            raise pytest.UsageError("No args project_id or test_run")

    def get_test_run(self) -> int:
        return self.test_run

    @lru_cache(16)
    def get_case_ids(self, test_run_id: int) -> List[int]:
        return [i["case_id"] for i in self.api.tests.get_tests(test_run_id)]

    def _format_string(self, value: str) -> str:
        try:
            _datetime = self.__date_time.strftime(self.date_format)
        except (ValueError, TypeError):
            _datetime = self.__date_time.isoformat(sep=" ")
        data = _Dict(datetime=_datetime, __version__=__version__)
        data.update(getattr(self._conf, "_metadata", {}))
        return value.format_map(data)

    def close(self):
        if self.close_on_complete:
            self.api.runs.close_run(self.test_run)
