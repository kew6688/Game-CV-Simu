from multiprocessing import Process, set_start_method, Queue
from simul_control import control
from screen_grab import grab_screen_win32
from obj_detect import Detector
import time
import cv2
import numpy as np
import argparse

window_size = 640
screen_resolution = (1920, 1080)
game_title = "Apex Legends"
grab_rect = (screen_resolution[0]//2-window_size//2, screen_resolution[1]//2-window_size//2, window_size, window_size)

def nearest_obj(obj_lst):
    dist_min = window_size**2 *2
    pos_min = (0,0)
    for obj in obj_lst:
        x,y = int(obj[1] * window_size), int(obj[2] * window_size)
        d = (x - window_size//2)**2 + (y - window_size//2)**2
        if d < dist_min:
            dist_min = d
            pos_min = (x - window_size//2,y - window_size//2)
    return pos_min

def draw_rect(img, bl):
    for obj in bl:
        x,y = obj[1] * window_size, obj[2] * window_size
        w,h = obj[3] * window_size, obj[4] * window_size
        x1,y1 = int(x-w/2), int(y-h/2)
        cv2.rectangle(img, (x1,y1), (int(x1+w),int(y1+h)), (0, 0, 255), 2)
        cv2.putText(img,f'{obj[0]}_{obj[5]}%',(x1,y1),cv2.FONT_HERSHEY_COMPLEX,0.8,(0, 255, 0), 2)
    
def draw_fps(img,fps,t):
    if len(fps)>9:
        fps.pop(0)
    cur = time.time()
    fps.append(1 / (cur-t+1e-5))
    # print(fps)
    cv2.putText(img,f'FPS: {int(np.mean(fps))}',(20,40),cv2.FONT_HERSHEY_COMPLEX,0.8,(0, 0, 255), 2)

def main():
    set_start_method('spawn')
    q = Queue()
    p = Process(target=control, args=(q,))
    p.start()

    # initialize model
    m = Detector()  #TODO


    fps = []
    # main loop starts
    while True:
        t = time.time()

        # screen shot      
        img = grab_screen_win32(game_title, grab_rect)
        print(img.shape)

        # detect objects
        box_lst = m.inference_img(img)
        box_lst.append((1,0.5,0.4,0.2,0.4,50))
        # send position
        pos = nearest_obj(box_lst)
        q.put(pos)

        # draw rectangle, display FPS
        draw_rect(img, box_lst)
        draw_fps(img, fps, t)

        # show img
        cv2.imshow('OpenCV/Numpy normal', img)

        # Press "q" to quit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

        # time.sleep(1)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # parser.add_argument('--model', default='yolov/ 'assets/bus.jpg'), help='Path to input image.')
    args = parser.parse_args()
    main()