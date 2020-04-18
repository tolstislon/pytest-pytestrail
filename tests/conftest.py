import pytest
import responses


@pytest.fixture
def mock():
    with responses.RequestsMock() as rsps:
        yield rsps
