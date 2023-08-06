import threading
import time
from pynput.mouse import Button, Listener, Controller
from pynput import keyboard, mouse
import pynput
import pyautogui
import queue
import multiprocessing
import pydirectinput

left_pressed = False
right_pressed = False
aim_sensitive = 1
flag_lock = False
shot_interval = 0.1
space_pressed = False
exit = False


def poppy():
    global space_pressed
    # pydirectinput.keyDown('c')
    pydirectinput.PAUSE=0.02
    while space_pressed:
        # print('poppy')
        pydirectinput.press('space')
        # pydirectinput.mouse.scroll(0,2)
    # pydirectinput.keyUp('c')

# keyboard listener
def on_press(key):
    global flag_lock,space_pressed,exit
    try:
        # print(key)
        if key == keyboard.KeyCode.from_char('f'):
            flag_lock = True
            # print(f'aimbot: {flag_lock}')
        if key == keyboard.Key.end:
            exit = True
        # if key == keyboard.Key.space:
        #     print(key)
        # if key == keyboard.Key.ctrl_l:
        #     # print("start poppy")
        #     if space_pressed:
        #         return
        #     space_pressed = True
        #     th = threading.Thread(target=poppy)
        #     th.start()
    except AttributeError: 
        print(f'special key {key} pressed')

def on_release(key):
    global flag_lock
    # print("release",key)
    if key == keyboard.KeyCode.from_char('f'):
        flag_lock = False
    return

# mouse listener
def on_move(x,y):
    # print(f'cursor moved to {(x,y)}')
    return

def on_click(x,y,button,pressed):
    global left_pressed,right_pressed
    if pressed:
        if button == mouse.Button.left:
            left_pressed = True
        elif button == mouse.Button.right:
            right_pressed = True
    else:
        if button == mouse.Button.left:
            left_pressed = False
        elif button == mouse.Button.right:
            right_pressed = False
    print('{2} is {0} at {1}, left pressed {3} right pressed {4} '.format('Pressed' if pressed else 'Released', (x,y), button, left_pressed, right_pressed))
    
def on_scroll(x,y,dx,dy):
    return

def control(q):
    global mouse_aim,exit
    pydirectinput.PAUSE=0.01
    # prepare keyboard listener
    # with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    #     listener.join()
    # with mouse.Listener(on_press=on_press, on_release=on_release) as listener:
    #     listener.join()
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    # mouse_listener = mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)
    # mouse_listener.start()
    while True:
        if flag_lock or left_pressed and right_pressed:
            try:
                pos = q.get_nowait()
                # print(pos)
                mouse_aim = (int(pos[0] / aim_sensitive), int(pos[1] / aim_sensitive))
                pydirectinput.moveRel(*mouse_aim, relative=True)
            except multiprocessing.queues.Empty:
                pass  
            # while not q.empty():
            #     pos = q.get()
            #     print(pos)
            #     mouse_aim = (int(pos[0] / aim_sensitive), int(pos[1] / aim_sensitive))
            #     pydirectinput.moveRel(*mouse_aim, relative=True)

        # test
        # if not q.empty():
        #     mouse_aim = q.get()
        #     print(mouse_aim)
        #     pydirectinput.moveRel(*mouse_aim, relative=True)

        if exit:
            break
        

def main():
    global exit
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    mouse_listener = mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)
    mouse_listener.start()
    while not exit:
        pass
    # q = Queue()
    # control(q)

if __name__ == '__main__':  
    main()

# screen = (2736,1824)
# pyautogui.moveTo(screen)