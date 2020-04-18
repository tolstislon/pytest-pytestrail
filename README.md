[![PyPI](https://img.shields.io/pypi/v/pytest-pytestrail?color=yellow&label=version)](https://pypi.org/project/pytest-pytestrail/)
[![Downloads](https://pepy.tech/badge/pytest-pytestrail)](https://pepy.tech/project/pytest-pytestrail)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pytest-pytestrail.svg)](https://pypi.org/project/pytest-pytestrail/)
[![Pytest Version](https://img.shields.io/badge/pytest-%3E%3D3.8-blue.svg)](https://github.com/pytest-dev/pytest/releases)
[![Build Status](https://travis-ci.com/tolstislon/pytest-pytestrail.svg?branch=master)](https://travis-ci.com/tolstislon/pytest-pytestrail)

# pytest-pytestrail

Pytest plugin for interaction with TestRail


### Install

```shell
pip install pytest-pytestrail
```

### Example

```python
from pytest_pytestrail import pytestrail


@pytestrail.case('C32')
def test_one():
    assert True

@pytestrail.case('C12')
def test_two():
    assert True
```

###### Steps
```python
from pytest_pytestrail import pytestrail

case = pytestrail.steps_case('C3')

@case.step(1)
def test_step_one():
    assert True


@case.step(2)
def test_step_two():
    assert True
```

###### Steps parametrize
```python
from pytest_pytestrail import pytestrail
import pytest

@pytest.mark.parametrize('data', pytestrail.params('C84', [1, 23, 33, 1, 57]))
def test_five(data):
    assert data

@pytest.mark.parametrize('data', [pytestrail.param(1, 'C55'), pytestrail.param(2, 'C56')])
def test_six(data):
    assert data
```

#### Configuration

Support environment variables
* TESTRAIL_URL
* TESTRAIL_EMAIL
* TESTRAIL_PASSWORD



##### Config file

`pytest.ini` or `setup.cfg` [pytest configuration](https://docs.pytest.org/en/latest/customize.html)

```ini
[pytest]
pytestrail (bool):                       Enable plugin
pytestrail-url (string):                 TestRail address
pytestrail-email (string):               Email for the account on the TestRail
pytestrail-password (string):            Password for the account on the TestRail
pytestrail-test-run (string):            ID testrun
pytestrail-no-decorator-skip (bool):     Skip tests without decorator
pytestrail-report (bool):                Enable report
pytestrail-no-ssl-check (bool):          Do not check for valid SSL certificate on TestRail host
pytestrail-project-id (string):          ID of the project
pytestrail-suite-id (string):            ID of the test suite
pytestrail-testrun-name (string):        Name given to testrun, that appears in TestRail
pytestrail-date-format (string):         Date format (default: %Y-%m-%d %H:%M:%S)
pytestrail-tz-local (bool):              Use local time zone (Default: UTC)
pytestrail-close-on-complete (bool):     Close test run on completion
pytestrail-milestone-id (string):        Set test tun milestone
pytestrail-testrun-description (string): Description given to testrun, that appears in TestRail
```

or

##### Command line options

```bash
--pytestrail                                    Enable plugin
--tr-url=TR_URL                                 TestRail address
--tr-email=TR_EMAIL                             Email for the account on the TestRail
--tr-password=TR_PASSWORD                       Password for the account on the TestRail
--tr-test-run=TR_TEST_RUN                       ID testrun
--tr-no-decorator-skip                          Skip tests without decorator
--tr-report                                     Enable report
--tr-no-ssl-check                               Do not check for valid SSL certificate on TestRail host
--tr-project-id=TR_PROJECT_ID                   ID of the project
--tr-suite-id=TR_SUITE_ID                       ID of the test suite
--tr-testrun-name=TR_TESTRUN_NAME               Name given to testrun, that appears in TestRail
--tr-date-format=TR_DATE_FORMAT                 Date format (default: %Y-%m-%d %H:%M:%S)
--tr-tz-local                                   Use local time zone (Default: UTC)
--tr-close-on-complete                          Close test run on completion
--tr-milestone-id=TR_MILESTONE_ID               Set test tun milestone
--tr-testrun-description=TR_TESTRUN_DESCRIPTION Description given to testrun, that appears in TestRail
```
