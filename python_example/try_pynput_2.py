from pynput import keyboard
from pydub import AudioSegment
from pydub.playback import play
import threading
import time
import random
import os


# # 检查声音文件是否存在
SOUND_FOLDER = "wood_fish"
SOUND_LIST = []
for root, dirs, files in os.walk(SOUND_FOLDER):
    for f in files:
        if f.endswith(".mp3"):
            file_path = os.path.join(root, f)
            SOUND_LIST.append(file_path)

print(SOUND_LIST)

last_key_time = 0
def on_press(key):
    global last_key_time
    current_time = time.time()
    # 防抖：忽略 0.5 秒内的重复事件
    if current_time - last_key_time < 0.5:
        return
    last_key_time = current_time
    # key_char = key.char.lower()
    # print(f"user input: {key_char}")
    try:
        sound_file = random.choice(SOUND_LIST)
        try:
            play_sound(sound_file)
        except Exception as e:
            print(f"无法播放声音 {sound_file}: {e}")
    except AttributeError:
        # 忽略特殊键（如Shift、Ctrl等）
        pass

def play_sound(sound_file):
    print(f"paly sound_file:{sound_file}")
    # 播放对应的声音
    sound_file = AudioSegment.from_file(sound_file)
    clipped_sound = sound_file[:1000]  # 截取前1000毫秒
    threading.Thread(target=play, args=(clipped_sound,)).start()

def on_release(key):
    # 按ESC键停止监听
    if key == keyboard.Key.esc:
        print("停止监听...")
        return False

#启动键盘监听
print("开始监听键盘输入（按ESC键退出）...")
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
