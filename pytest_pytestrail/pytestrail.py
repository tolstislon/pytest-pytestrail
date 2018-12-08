import pytest


def case(*args):
    return pytest.mark.pytestrail(*args)
