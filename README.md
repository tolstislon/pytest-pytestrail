[![GitHub version](https://badge.fury.io/gh/tolstislon%2Fpytest-pytestrail.svg)](https://badge.fury.io/gh/tolstislon%2Fpytest-pytestrail)
[![Downloads](https://pepy.tech/badge/pytest-pytestrail)](https://pepy.tech/project/pytest-pytestrail)

# pytest-pytestrail

Pytest plugin for interaction with TestRail

### Requirements

* python 3.6+
* pytest 3.8+

### Install

```shell
pip install pytest-pytestrail
```

### Example

```python
from pytest_pytestrail import pytestrail


@pytestrail.case('C12')
def test_one():
    # test code

@pytestrail.case('C13', 'C14')
def test_two():
    # test code
```

#### Configuration

##### Config file

`pytest.ini` or `setup.cfg` [pytest configuration](https://docs.pytest.org/en/latest/customize.html)

```ini
[pytest]
pytestrail = True  
pytestrail-url = https://exemle.testrail.com/
pytestrail-email = exemle@mail.com
pytestrail-password = password
pytestrail-test-run = 12
pytestrail-no-decorator-skip = True
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
```
