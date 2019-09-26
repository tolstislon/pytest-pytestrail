![PyPI](https://img.shields.io/pypi/v/pytest-pytestrail?color=yellow&label=version)
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
