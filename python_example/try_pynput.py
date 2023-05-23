from pynput import keyboard
from pynput import mouse
import pyautogui
import itertools
import time
import sys

def gen_list(start_point, max_range, delta):
    L = []
    # forward direction
    for i in range(start_point, max_range, delta):
        L.append(i)
    # reverse direction
    for j in range(start_point, 0, -delta):
        L.append(j)
    return sorted(set(L))

def matrix_click(x,y):
    x_list = gen_list(x, width, d_width)
    y_list = gen_list(y, height, d_height)
    print(x_list)
    print(y_list)
    print(list(itertools.product(x_list, y_list)))

def on_press(key):
    """定义按下时候的响应，参数传入key"""
    try:
        print(f'{key.char} down')
    except AttributeError:
        print(f'{key} down')


def on_release(key):
    """定义释放时候的响应"""
    print(f'{key} up')

def on_click(x,y,button,pressed):
    print('click at',x,y,button,pressed)

# 监听写法1
def listen_key_block():
    with keyboard.Listener(
            on_press=on_press, on_release=on_release) as listener:
        listener.join()  # 加入线程池，阻塞写法


# 监听写法2
def listen_key_nblock():
    listener = keyboard.Listener(
        on_press=on_press, on_release=on_release
    )
    listener.start()  # 启动线程
 
def listen_mouse_nblock():
    listener = mouse.Listener(on_click=on_click,)
    listener.start()
 
 
if __name__ == '__main__':
    width, height = pyautogui.size()
    n_width = 4
    n_height = 3
    d_width = width // n_width
    d_height = height // n_height
    print(f"屏幕分辨率： {width} x {height}")
    print(f"等分成： {n_width} x {n_height} 份")
    print(f"每份宽 x 高： {d_width} x {d_height}")
    print(f"原始点击位置： (800, 500)")
    print("其他相似点：")
    matrix_click(800, 500)
    sys.exit(0)
    listen_mouse_nblock()
    listen_key_nblock()
    while True: # 这里应该用一个循环维持主线程，否则主线程结束了子线程就自动结束了
        pass
