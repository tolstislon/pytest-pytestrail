import abc
import threading
import time
from enum import Enum
from queue import Queue
from typing import Dict, List, Optional, Tuple, Union

from _pytest.reports import TestReport
from testrail_api import TestRailAPI

from ._case import Case
from ._constants import STATUS


class SIGNAL(Enum):
    STOP = "STOP"


class Report(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get(self) -> dict:
        pass


class ReportCase(Report):
    def __init__(self, case: Case, report: TestReport) -> None:
        self.case = case
        self.report = report

    def get_id(self) -> int:
        return self.case.case_id

    @staticmethod
    def pars_comment(comment: Optional[str]) -> str:
        if comment is None:
            return ""
        data = comment.__str__().split("\n")
        return "\n".join(["\t{}".format(line) for line in data])

    def get_step(self) -> Tuple[Dict[str, Union[str, int]], float]:
        return (
            {
                "content": "Step {}".format(self.case.step),
                "status_id": STATUS[self.report.outcome],
                "actual": self.pars_comment(self.report.longrepr),
            },
            self.report.duration,
        )

    def get(self) -> Dict[str, Union[str, int]]:
        return {
            "case_id": self.case.case_id,
            "status_id": STATUS[self.report.outcome],
            "comment": self.pars_comment(self.report.longrepr),
            "elapsed": time.strftime(
                "%Mm %Ss", time.gmtime(round(self.report.duration) or 1)
            ),
        }


class ReportStep(Report):
    def __init__(self, data: List[ReportCase]) -> None:
        self.steps = data

    def get(self) -> Dict[str, Union[str, int, list]]:
        step_results = []
        elapsed = 0  # type: float
        status_id = STATUS["passed"]
        for step in self.steps:
            result, duration = step.get_step()
            step_results.append(result)
            elapsed += duration
            if result["status_id"] > status_id:
                status_id = result["status_id"]
        case_id = self.steps[-1].get_id()
        return {
            "case_id": case_id,
            "status_id": status_id,
            "comment": "",
            "elapsed": time.strftime("%Mm %Ss", time.gmtime(round(elapsed) or 1)),
            "custom_step_results": step_results,
        }


_REPORT = Union[ReportCase, ReportStep]


class Sender(threading.Thread):
    def __init__(self, api: TestRailAPI, run_id: int, **kwargs) -> None:
        self.__api = api
        self.__run_id = run_id
        self.__kwargs = {k: v for k, v in kwargs.items() if v}
        self.__queue = Queue()  # type: Queue
        self.__steps = {}  # type: Dict[int, list]
        super().__init__(target=self.__worker, args=())

    def send(self, case: Case, report: TestReport) -> None:
        rep = self.__create_report(case, report)
        if rep is not None:
            self.__queue.put(rep)

    def __create_report(self, case: Case, report: TestReport) -> Optional[_REPORT]:
        rep = ReportCase(case, report)
        if case.is_step:
            data = self.__steps.setdefault(case.case_id, [])
            data.append(rep)
            if case.is_last:
                report_steps = ReportStep(data)
                del self.__steps[case.case_id]
                return report_steps
            return None
        return rep

    def __worker(self) -> None:
        while True:
            data = self.__queue.get()
            if data is SIGNAL.STOP:
                break
            elif isinstance(data, Report):
                request = data.get()
                request["run_id"] = self.__run_id
                request.update(self.__kwargs)
                try:
                    self.__api.results.add_result_for_case(**request)
                except Exception:  # noqa
                    pass

    def stop(self) -> None:
        self.__queue.put(SIGNAL.STOP)
        print("\nCompleting Report Upload ...")
        self.join()

    @property
    def queue_size(self) -> int:
        return self.__queue.qsize()


class FakeSender:
    def __init__(self, *args, **kwargs):
        pass

    def send(self, *args, **kwargs) -> None:
        pass

    def stop(self) -> None:
        pass

    def join(self) -> None:
        pass

    @staticmethod
    def is_alive() -> bool:
        return False

    @property
    def queue_size(self) -> int:
        return 0
