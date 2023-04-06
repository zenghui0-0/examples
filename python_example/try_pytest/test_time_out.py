from  func_timeout import  func_set_timeout, FunctionTimedOut
import pytest
import time


@func_set_timeout(2.5)
def test_func_timeout():
    time.sleep(5)
    assert True, "run passed"

