from testrail_api import TestRailAPI


class Config:
    api: TestRailAPI

    def __init__(self, conf) -> None:
        self.url = conf.getoption('--tr-url') or conf.getini('pytestrail-url')
        self.email = conf.getoption('--tr-email') or conf.getini('pytestrail-email')
        self.password = conf.getoption('--tr-password') or conf.getini('pytestrail-password')
        self.test_run = conf.getoption('--tr-test-run') or conf.getini('pytestrail-test-run')
        self.report = conf.getoption('--tr-report') or conf.getini('pytestrail-report')
        self.no_decorator_skip = conf.getoption('--tr-no-decorator-skip') or conf.getini('pytestrail-no-decorator-skip')

        self.work()

    def work(self) -> None:
        self.api = TestRailAPI(self.url, self.email, self.password)
        if not self.test_run:
            raise ValueError(f'Invalid value test-run {self.test_run}')

    def get_test_run(self) -> int:
        return self.test_run

    def get_case_ids(self):
        return [i['case_id'] for i in self.api.tests.get_tests(self.test_run)]
