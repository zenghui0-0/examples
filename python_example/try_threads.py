import time
import threading

def test(a):
    while True:
        print("sleep {} test".format(a))
        time.sleep(a)


test1 = threading.Thread(target=test, args=((1,)))
test1.start()

test2 = threading.Thread(target=test, args=((2,)))
test2.start()
test2.join()