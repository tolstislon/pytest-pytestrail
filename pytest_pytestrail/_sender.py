import abc
import threading
import time
from queue import Queue
from typing import List, Tuple, Optional

from ._case import Case
from ._constants import STATUS
from requests.exceptions import RequestException


class Report(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get(self) -> dict:
        pass


class ReportCase(Report):

    def __init__(self, case, report):
        self.case = case
        self.report = report

    def get_id(self) -> int:
        return self.case.case_id

    @staticmethod
    def pars_comment(comment: Optional[str]) -> str:
        if comment is None:
            return ''
        data = comment.__str__().split('\n')
        return '\n'.join([f'\t{line}' for line in data])

    def get_step(self) -> Tuple[dict, float]:
        return {'content': f'Step {self.case.step}',
                'status_id': STATUS[self.report.outcome],
                'actual': self.pars_comment(self.report.longrepr)
                }, self.report.duration

    def get(self) -> dict:
        return {
            'case_id': self.case.case_id,
            'status_id': STATUS[self.report.outcome],
            'comment': self.pars_comment(self.report.longrepr),
            'elapsed': time.strftime('%Mm %Ss', time.gmtime(round(self.report.duration) or 1))
        }


class ReportStep(Report):

    def __init__(self, data: List[ReportCase]):
        self.steps = data

    def get(self):
        step_results = []
        elapsed = 0
        status_id = STATUS['passed']
        for step in self.steps:
            result, duration = step.get_step()
            step_results.append(result)
            elapsed += duration
            if result['status_id'] > status_id:
                status_id = result['status_id']
        case_id = self.steps[-1].get_id()
        return {
            'case_id': case_id,
            'status_id': status_id,
            'comment': '',
            'elapsed': time.strftime('%Mm %Ss', time.gmtime(round(elapsed) or 1)),
            'custom_step_results': step_results
        }


class Sender(threading.Thread):

    def __init__(self, api, run_id, **kwargs):
        self._api = api
        self.run_id = run_id
        self._kwargs = {k: v for k, v in kwargs.items() if v}
        self._queue = Queue()
        self._steps = {}
        super().__init__(target=self.worker, args=())

    def send(self, case: Case, report):
        rep = self._create_report(case, report)
        if rep is not None:
            self._queue.put(rep)

    def _create_report(self, case: Case, report):
        if case.is_step:
            data = self._steps.setdefault(case.case_id, [])
            rep = ReportCase(case, report)
            data.append(rep)
            if case.is_last:
                report_steps = ReportStep(data)
                del self._steps[case.case_id]
                return report_steps
            else:
                return None
        else:
            return ReportCase(case, report)

    def worker(self):
        while True:
            data = self._queue.get()
            if isinstance(data, Report):
                request = data.get()
                request['run_id'] = self.run_id
                request.update(self._kwargs)
                try:
                    self._api.results.add_result_for_case(**request)
                except RequestException:
                    pass
            else:
                break

    def stop(self):
        self._queue.put('stop')
        self.join()


class FakeSender:

    def __init__(self, *args, **kwargs):
        pass

    def send(self, *args, **kwargs):
        pass

    def stop(self):
        pass

    def join(self):
        pass
