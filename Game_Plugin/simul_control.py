import threading
import time
from pynput.mouse import Button, Listener, Controller
from pynput import keyboard, mouse
import pynput
import pyautogui
import queue
import multiprocessing
from multiprocessing import Process, Event
import pydirectinput

left_pressed = False
right_pressed = False
aim_sensitive = 0.6
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
        # if key == keyboard.KeyCode.from_char('f'):
        if key == keyboard.Key.alt_l:
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
    # if key == keyboard.KeyCode.from_char('f'):
    if key == keyboard.Key.alt_l:
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

def proc(flag_event, flag_event2):
    # keyboard listener
    def on_press(key):
        global flag_lock,space_pressed,exit
        try:
            if key == keyboard.Key.alt_l:
                flag_event.set()
                print('set flag')
        except AttributeError: 
            print(f'special key {key} pressed')

    def on_release(key):
        if key == keyboard.Key.alt_l:
            flag_event.clear()
        return
    
    def on_click(x,y,button,pressed):
        if pressed:
            if button == mouse.Button.left:
                flag_event.set()
            elif button == mouse.Button.right:
                flag_event2.set()
        else:
            if button == mouse.Button.left:
                flag_event.clear()
            elif button == mouse.Button.right:
                flag_event2.clear()
        # print('{2} is {0} at {1}'.format('Pressed' if pressed else 'Released', (x,y), button))

    # with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    #     listener.join()

    with mouse.Listener(on_click=on_click) as listener:
        listener.join()
    
def control(q):
    global mouse_aim,exit
    pydirectinput.PAUSE=0

    # start mouse listener from second process
    flag_event1 = Event()
    flag_event2 = Event()
    proc1 = Process(target=proc, args=(flag_event1, flag_event2))
    proc1.start()

    while True:
        if flag_event1.is_set() and flag_event2.is_set():
            try:
                pos = q.get_nowait()
                # print(pos)
                mouse_aim = (int(pos[0] / aim_sensitive), int(pos[1] / aim_sensitive))
                # t = time.time()
                pydirectinput.moveRel(*mouse_aim, relative=True)
                # print(f'{(time.time()-t)*1000:.2f} ms')
            except multiprocessing.queues.Empty:
                pass  
        

def main():
    global exit
    # prepare keyboard listener
    # with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    #     listener.join()
    # with mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as listener:
    #     listener.join()
    # listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    # listener.start()
    # mouse_listener = mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)
    # mouse_listener.start()
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    mouse_listener = mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)
    mouse_listener.start()
    while not exit:
        pass

if __name__ == '__main__':  
    main()
