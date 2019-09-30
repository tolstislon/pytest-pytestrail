from typing import Dict

PYTESTRAIL_MARK: str = 'pytestrail'
PYTESTRAIL_CASE_MARK: str = 'pytestrail_case'

STATUS: Dict[str, int] = {
    "passed": 1,
    "skipped": 2,
    "failed": 5
}
