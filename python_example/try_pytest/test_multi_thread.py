import os
import time
import pytest
import random
import threading

def three_d_mark(run_time):
    print("[os_tests] 3dmark running...")
    time.sleep(run_time)
    print("[os_tests] 3dmark finished.")
    return random.randint(0,1)


def memory_leak(run_time):
    print("[os_tests] memory_leak running...")
    time.sleep(run_time)
    print("[os_tests] memory_leak finished.")
    return random.randint(0,1)



class MyThread(threading.Thread):

    def __init__(self, func, args=()):
        super().__init__()
        self.func = func
        self.args = args
        self.result = 0

    def run(self):
        self.result = self.func(*self.args)

    def join(self):
        threading.Thread.join(self)
        try:
            return self.result
        except Exception:
            return None 

@pytest.mark.parametrize('td_time, ml_time', [(30, 20)])
def test_threads_join(td_time, ml_time):
    """
    3dmark memoryleak should both end normally, 
    before test case end
    """
    t_3dmark = MyThread(three_d_mark, [td_time])
    t_3dmark.start()
    t_memoryleak = MyThread(memory_leak, [ml_time])
    t_memoryleak.start()
    #ret1 = t_3dmark.join()
    #ret2 = t_memoryleak.join()
    assert False, f'Failed, 3dmark return: {ret1}, memoryleak return: {ret2}'
    print("Test 3dmark, memoryleak PASSED.")


def test_threads_faild_beak():
    """
    3dmark or memoryleak should both end 
    when one of them got failure
    then test case end
    """
    pass


def test_threads_force_beak():
    """
    fore all test thread end by a signal
    then test case end
    """
    pass


if __name__ == "__main__":
    test_threads_join(30, 20)