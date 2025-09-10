import pytest

from python_test.data_helpers.api_helpers import SpendsHttpClient
from python_test.databases.spend_db import SpendDb
from python_test.databases.userdata_bd import UserdataDb
from python_test.model.config import Envs


@pytest.fixture(scope="session")
def spends_client(envs: Envs, auth_token: str) -> SpendsHttpClient:
    return SpendsHttpClient(envs.gateway_url, auth_token, envs.test_username)


@pytest.fixture(scope="session")
def spend_db(envs: Envs) -> SpendDb:
    return SpendDb(envs)


@pytest.fixture(scope="session")
def userdata_db(envs: Envs) -> UserdataDb:
    return UserdataDb(envs)
