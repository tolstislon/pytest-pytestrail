[![GitHub version](https://badge.fury.io/gh/tolstislon%2Fpytest-pytestrail.svg)](https://badge.fury.io/gh/tolstislon%2Fpytest-pytestrail)
[![Downloads](https://pepy.tech/badge/pytest-pytestrail)](https://pepy.tech/project/pytest-pytestrail)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pytest-pytestrail.svg)
![Pytest Version](https://img.shields.io/badge/pytest-%3E%3D3.8-blue.svg)

# pytest-pytestrail

Pytest plugin for interaction with TestRail


### Install

```shell
pip install pytest-pytestrail
```

### Example

```python
from pytest_pytestrail import pytestrail


@pytestrail.case('C12')
def test_one():
    ... # test code

@pytestrail.case('C13')
def test_two():
    ... # test code
```

###### Steps
```python
from pytest_pytestrail import pytestrail

case = pytestrail.steps_case('C2')

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

# pytestrail.param(value, case, step)
@pytest.mark.parametrize('data', [pytestrail.param(1, 'C5', 1), pytestrail.param(2, 'C5', 2)])
def test_four(data):
    assert data
```

#### Configuration

##### Config file

`pytest.ini` or `setup.cfg` [pytest configuration](https://docs.pytest.org/en/latest/customize.html)

```ini
[pytest]
pytestrail = True  
pytestrail-url = https://example.testrail.com
pytestrail-email = exemle@mail.com
pytestrail-password = password
pytestrail-test-run = 12
pytestrail-no-decorator-skip = True
pytestrail-report = True
```

or

##### Command line options

```shell
--pytestrail            Enable plugin
--tr-url=URL            TestRail address
--tr-email=EMAIL        Email for the account on the TestRail
--tr-password=PASSWORD  Password for the account on the TestRail
--tr-test-run=12        ID testrun
--tr-no-decorator-skip  Skip tests without decorator
--tr-report             Enable report
```
