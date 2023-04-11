import pytest

@pytest.fixture(params='case_name')
def try_fixture(request):
    print(f"run setup for case: {request.param}")
    yield
    print(f"run tear down for case: {request.param}")