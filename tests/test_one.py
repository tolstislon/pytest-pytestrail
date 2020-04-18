import re
import pytest
import responses

pytest_plugins = ("pytester",)

TESTS = """
        from pytest_pytestrail import pytestrail
        
        @pytestrail.case("C1")
        def test_one():
            assert True
            
        @pytestrail.case("C2")
        def test_two():
            assert True
            
        @pytestrail.case("C3")
        def test_three():
            assert True
        """


def test_start(testdir, mock):
    mock.add(
        responses.GET,
        'http://testrail.com/index.php?/api/v2/get_tests/1',
        body='[{"case_id": 1}, {"case_id": 2}, {"case_id": 3}]',
        status=200,
        content_type='application/json'
    )
    testdir.makepyfile(TESTS)
    result = testdir.runpytest(
        '--pytestrail',
        '--tr-url=http://testrail.com',
        '--tr-email=email@mail.com',
        '--tr-password=password',
        '--tr-test-run=1'
    )
    assert result.ret == 0
    result.assert_outcomes(passed=3)
    stdout = result.stdout.str()
    assert re.search(r'PyTestRail .+: ON', stdout)


def test_start_ini(testdir, mock):
    mock.add(
        responses.GET,
        'http://testrail.com/index.php?/api/v2/get_tests/1',
        body='[{"case_id": 1}, {"case_id": 2}, {"case_id": 3}]',
        status=200,
        content_type='application/json'
    )
    testdir.makeini(
        """
        [pytest]
        pytestrail=true
        pytestrail-url=http://testrail.com
        pytestrail-email=email@mail.com
        pytestrail-password=password
        pytestrail-test-run=1
        """
    )
    testdir.makepyfile(TESTS)
    result = testdir.runpytest()
    assert result.ret == 0
    result.assert_outcomes(passed=3)
    stdout = result.stdout.str()
    assert re.search(r'PyTestRail .+: ON', stdout)


def test_deselected(testdir, mock):
    mock.add(
        responses.GET,
        'http://testrail.com/index.php?/api/v2/get_tests/12',
        body='[{"case_id": 1}]',
        status=200,
        content_type='application/json'
    )
    testdir.makepyfile(TESTS)
    result = testdir.runpytest(
        '--pytestrail',
        '--tr-url=http://testrail.com',
        '--tr-email=email@mail.com',
        '--tr-password=password',
        '--tr-test-run=12'
    )
    assert result.ret == 0
    result.assert_outcomes(passed=1)


def test_deselected_ini(testdir, mock):
    mock.add(
        responses.GET,
        'http://testrail.com/index.php?/api/v2/get_tests/12',
        body='[{"case_id": 1}]',
        status=200,
        content_type='application/json'
    )
    testdir.makeini(
        """
        [pytest]
        pytestrail=true
        pytestrail-url=http://testrail.com
        pytestrail-email=email@mail.com
        pytestrail-password=password
        pytestrail-test-run=12
        """
    )
    testdir.makepyfile(TESTS)
    result = testdir.runpytest()
    assert result.ret == 0
    result.assert_outcomes(passed=1)


def test_disable_plugin(testdir):
    testdir.makepyfile(TESTS)
    result = testdir.runpytest(
        '--tr-url=http://testrail.com',
        '--tr-email=email@mail.com',
        '--tr-password=password',
        '--tr-test-run=12'
    )
    assert result.ret == 0
    result.assert_outcomes(passed=3)
    stdout = result.stdout.str()
    assert re.search(r'pytestrail-[\w.]+', stdout)
    assert not re.search(r'PyTestRail [\w.]+: ON', stdout)


def test_disable_plugin_ini(testdir):
    testdir.makeini(
        """
        [pytest]
        pytestrail-url=http://testrail.com
        pytestrail-email=email@mail.com
        pytestrail-password=password
        pytestrail-test-run=12
        """
    )
    testdir.makepyfile(TESTS)
    result = testdir.runpytest()
    assert result.ret == 0
    result.assert_outcomes(passed=3)
    stdout = result.stdout.str()
    assert re.search(r'pytestrail-[\w.]+', stdout)
    assert not re.search(r'PyTestRail [\w.]+: ON', stdout)


def test_parametrize_many_cases(testdir, mock):
    mock.add(
        responses.GET,
        'http://testrail.com/index.php?/api/v2/get_tests/1',
        body='[{"case_id": 55}, {"case_id": 57}]',
        status=200,
        content_type='application/json'
    )
    testdir.makepyfile(
        """
        import pytest
        from pytest_pytestrail import pytestrail
        @pytest.mark.parametrize('data', [
            pytestrail.param(1, 'C55'), 
            pytestrail.param(2, 'C56'), 
            pytestrail.param(3, 'C57')
        ])
        def test_one(data):
            assert data
        """
    )
    result = testdir.runpytest(
        '--pytestrail',
        '--tr-url=http://testrail.com',
        '--tr-email=email@mail.com',
        '--tr-password=password',
        '--tr-test-run=1'
    )
    assert result.ret == 0
    result.assert_outcomes(passed=2)
    stdout = result.stdout.str()
    version = tuple(int(i) for i in pytest.__version__.split('.'))
    if version > (3, 8, 0):
        assert re.search(r'3 items / 1 deselected / 2 selected', stdout)
    else:
        assert re.search(r'2 passed, 1 deselected', stdout)
