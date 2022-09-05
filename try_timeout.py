import requests
import eventlet
import time
 
eventlet.monkey_patch()

time_limit = 17 #set timeout time 3s

flag = False

def SLEEP():
    time.sleep(5)

with eventlet.Timeout(time_limit,False):
    #assert False, "you failed at line12"
    SLEEP()
    #r=requests.get("https://me.csdn.net/dcrmg", verify=False)
    print('error')
print('over')
