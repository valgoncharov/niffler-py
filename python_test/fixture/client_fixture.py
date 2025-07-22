import pytest

from python_test.data_helpers.api_helpers import SpendsHttpClient
from python_test.databases.spend_db import SpendDb
from python_test.databases.usertdata_db import UserdataDb
from python_test.model.config import Envs


@pytest.fixture(scope="session")
def spends_client(envs: Envs, auth_token: str) -> SpendsHttpClient:
    return SpendsHttpClient(envs, auth_token)


@pytest.fixture(scope="session")
def spend_db(envs: Envs) -> SpendDb:
    return SpendDb(envs)


@pytest.fixture(scope="session")
def userdata_db(envs: Envs) -> UserdataDb:
    return UserdataDb(envs)