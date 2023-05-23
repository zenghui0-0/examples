from pynput import keyboard
from pynput import mouse
from pynput.mouse import Button
import pynput
import pyautogui
import itertools
import time
import sys

user_clieck_point = []

def gen_list(start_point, max_range, delta):
    L = []
    # forward direction
    for i in range(start_point, max_range, delta):
        L.append(i)
    # reverse direction
    for j in range(start_point, 0, -delta):
        L.append(j)
    return sorted(set(L))

def matrix_click(x, y):
    x_list = gen_list(x, width, d_width)
    y_list = gen_list(y, height, d_height)
    # print(x_list)
    # print(y_list)
    matrix_points = list(itertools.product(x_list, y_list))
    print(matrix_points)
    for matrix_point in matrix_points:
        if matrix_point[0] == x and matrix_point[1] == y:
            continue
        click_one(matrix_point[0], matrix_point[1])
        time.sleep(1)

def click_one(x,y):
    mouse_ctrl = mouse.Controller()
    print(f"send a click at {x} {y}")
    mouse_ctrl.position = (x, y)
    mouse_ctrl.press(Button.left)
    mouse_ctrl.release(Button.left)

def on_click(x,y,button,pressed):
    if not pressed:
        # Stop listener
        return False
    print('mouse click at:',x,y,button,pressed)
    if x < 0 or y < 0:
        return False
    global user_clieck_point
    user_clieck_point = [x, y]

def on_press(key):
    print(f'{key} down')
    if (key == pynput.keyboard.KeyCode(char = 's')):
        print(f'{key} key down, start running.')
        return False

# 加入线程池，阻塞写法监听键盘
def listen_key_block():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

# 阻塞式监听鼠标
def listen_mouse_block():
    with mouse.Listener(
            on_click=on_click) as listener:
        listener.join()
    return listener

def listen_mouse_nblock():
    listener = mouse.Listener(on_click=on_click)
    listener.start()
    return listener

if __name__ == '__main__':
    width, height = pyautogui.size()
    n_width = 4
    n_height = 3
    d_width = width // n_width
    d_height = height // n_height
    print(f"屏幕分辨率： {width} x {height}")
    print(f"等分成： {n_width} x {n_height} 份")
    print(f"每份宽 x 高： {d_width} x {d_height}")

    listen_key_block()
    while True:
        print("loop...")
        listener = listen_mouse_block()
        listener.stop()
        print(f"检测到用户点击位置：{user_clieck_point}")
        if len(user_clieck_point) == 2:
            matrix_click(user_clieck_point[0], user_clieck_point[1])
        time.sleep(2)
        user_clieck_point = []
