from pynput import keyboard
from pynput import mouse
from pynput.keyboard import Key
from pynput.mouse import Button



def on_press(key):
    """定义按下时候的响应，参数传入key"""
    try:
        print(f'{key.char} down')
    except AttributeError:
        print(f'{key} down')


def on_release(key):
    """定义释放时候的响应"""
    print(f'{key} up')


def on_move(x, y):
    print('move to', x, y)


def on_click(x, y, button, pressed):
    print('click at', x, y, button, pressed)


def on_scroll(x, y, dx, dy):
    print('scroll at', x, y, 'by', dx, dy)

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
    listener = mouse.Listener(
        on_move=None,  # 因为on_move太多输出了，就不放进来了，有兴趣可以加入
        on_click=on_click,
        on_scroll=on_scroll
    )
    listener.start()


class InputEvent():
    # 键盘
    # 生成了一个控制器类
    key_ctrl = keyboard.Controller()

    # 简单按下放松
    key_ctrl.press('a')
    key_ctrl.release('a')

    # 组合键写法1，顺序press，倒序release，比较麻烦
    key_ctrl.press(Key.shift)
    key_ctrl.press('a')
    key_ctrl.release(Key.shift)
    key_ctrl.release('a')

    # 组合键写法2，使用with，自动释放，代码量缩小一半
    with key_ctrl.pressed(Key.shift):
        key_ctrl.press('a')
        key_ctrl.release('a')

    # 整段文字输入
    key_ctrl.type('text')

    # 鼠标
    mouse_ctrl = mouse.Controller()
    mouse_ctrl.scroll(0, -1)  # 左右,上下，-1是往下滚，有小伙伴好奇，怎么能左右滚呢？
    # 当然是shift滚轮啦

    print(mouse_ctrl.position)
    mouse_ctrl.position = (0, 0)  # 绝对移动，直接设置坐标
    mouse_ctrl.move(80, 10)  # 相对移动，通过函数实现
    mouse_ctrl.click(Button.left, 1)  # 选择键和次数
    mouse_ctrl.press(Button.left)  # 按下与释放，选择键
    mouse_ctrl.release(Button.left)


if __name__ == '__main__':
    listen_mouse_nblock()
    listen_key_nblock()
    while True:  # 这里应该用一个循环维持主线程，否则主线程结束了子线程就自动结束了
        pass
