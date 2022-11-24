import time
import threading

def test(gap_time, total_time):
    start_time = 0
    while start_time < total_time:
        print("sleep {} test running, {} past...".format(gap_time, start_time))
        start_time += gap_time
        time.sleep(1)
        #time.sleep(gap_time)
    print("sleep {} test end.".format(gap_time))


test1 = threading.Thread(target=test, args=((1, 20)))
test1.start()

test2 = threading.Thread(target=test, args=((2, 20)))
test2.start()
#test2.join()