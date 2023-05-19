from pynput import keyboard
from pynput import mouse
 
def on_press(key):
    """定义按下时候的响应，参数传入key"""
    try:
        print(f'{key.char} down')
    except AttributeError:
        print(f'{key} down')
 
 
def on_release(key):
    """定义释放时候的响应"""
    print(f'{key} up')
 
def on_move(x,y):
    print('move to',x,y)
 
def on_click(x,y,button,pressed):
    print('click at',x,y,button,pressed)
 
def on_scroll(x,y,dx,dy):
    print('scroll at',x,y,'by',dx,dy)
 
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
        on_move=None, # 因为on_move太多输出了，就不放进来了，有兴趣可以加入
        on_click=on_click,
        on_scroll=on_scroll
    )
    listener.start()
 
 
if __name__ == '__main__':
    listen_mouse_nblock()
    listen_key_nblock()
    while True: # 这里应该用一个循环维持主线程，否则主线程结束了子线程就自动结束了
        pass
