from  func_timeout import  func_set_timeout, FunctionTimedOut
import pytest
import time
import os

case_name = os.path.basename(__file__).split(".")[0]

@func_set_timeout(2.5)
@pytest.mark.parametrize('try_fixture', [case_name], indirect=True)
def test_func_timeout(try_fixture):
    print(f"start testcase: {case_name}")
    time.sleep(5)
    assert True, f"testcase: {case_name} run passed"

