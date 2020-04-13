import pytest
import requests_mock


@pytest.fixture(scope="session")
def rmock():
    return requests_mock.Mocker()

