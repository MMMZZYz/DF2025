import pytest
from apis.login_api import login  # 确保路径没错

@pytest.fixture(scope="module")
def session():
    return login()
