import time
import pyautogui
from pynput.keyboard import Key, Controller
import cv2
import mss
import mss.tools
import numpy
import win32gui, win32ui, win32con, win32api

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import *
import win32gui
import sys
 
hwnd = win32gui.FindWindow(None, 'C:\Windows\system32\cmd.exe')
app = QApplication(sys.argv)
screen = QApplication.primaryScreen()
img = screen.grabWindow(hwnd).toImage()
img.save("screenshot.jpg")

# Reference: https://zhuanlan.zhihu.com/p/71533145
# use browser to visit http://www.trex-game.skipser.com/
# put the browser to the left side and run the programme

key = Controller()

web = (10, 10)
# pyautogui.moveTo(web)

tree1 = cv2.imread('tree1.png', 0)
# print(tree1.shape)
tw, th = tree1.shape[::-1]
# print(tw,th)

tree2 = cv2.imread('tree2.png', 0)
tw2, th2 = tree2.shape[::-1]

tree3 = cv2.imread('tree3.png', 0)
tw3, th3 = tree3.shape[::-1]

tree4 = cv2.imread('tree5.png', 0)
tw4, th4 = tree4.shape[::-1]

bird = cv2.imread('bird2.png', 0)
nw, nh = bird.shape[::-1]

# with mss.mss() as sct:
#     # Part of the screen to capture
#     monitor = {'top': 770, 'left': 220, 'width': 900, 'height': 300}
#     output = "sct-{top}x{left}_{width}x{height}.png".format(**monitor)
#     sct_img = sct.grab(monitor)
#     img = numpy.array(sct_img)
#     img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     res1 = cv2.matchTemplate(img_gray, tree1, cv2.TM_CCOEFF_NORMED)
#     threshold = 0.6
#     loc2 = numpy.where(res1 >= threshold)
#     for pt in zip(*loc2[::-1]):
#         print(pt)
#         cv2.rectangle(img, pt, (pt[0] + tw, pt[1] + th), (0, 0, 255), 2)
#     # Display the picture
#     while True:
#         cv2.imshow('OpenCV/Numpy normal', img)
#         if cv2.waitKey(25) & 0xFF == ord('q'):
#             cv2.destroyAllWindows()
#             break

def grab_screen_win32(window, rect=None):
    # hwnd = 0  # 窗口的编号，0号表示当前活跃窗口
    hwnd = win32gui.FindWindow(None, window)
    # 根据窗口句柄获取窗口的设备上下文DC（Divice Context）
    hwndDC = win32gui.GetWindowDC(hwnd)
    # 根据窗口的DC获取mfcDC
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    # mfcDC创建可兼容的DC
    saveDC = mfcDC.CreateCompatibleDC()
    # 创建bigmap准备保存图片
    saveBitMap = win32ui.CreateBitmap()
    if not rect:
        # 获取监控器信息
        MoniterDev = win32api.EnumDisplayMonitors(None, None)
        w = MoniterDev[0][2][2] * 2
        h = MoniterDev[0][2][3] * 2
        # start position
        x,y = 0,0
    else:
        x,y,w,h = rect
    #图片大小
    # print(w,h)

    # 为bitmap开辟空间
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    # 高度saveDC，将截图保存到saveBitmap中
    saveDC.SelectObject(saveBitMap)
    # 截取从左上角（x，y）长宽为（w，h）的图片
    saveDC.BitBlt((0, 0), (w, h), mfcDC, (x, y), win32con.SRCCOPY)
    img = numpy.frombuffer(saveBitMap.GetBitmapBits(True), dtype="uint8")
    img.shape = (h,w,4)
    img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
    # save img
    # saveBitMap.SaveBitmapFile(saveDC, "screenshot.jpg")

    # Free win
    win32gui.DeleteObject(saveBitMap.GetHandle())
    mfcDC.DeleteDC()
    saveDC.DeleteDC()

    return img

def startgame():
    pyautogui.click(web)
    time.sleep(0.03)
    pyautogui.keyDown('space')
    time.sleep(0.03)
    pyautogui.keyUp('space')
    print('game start')


def jump():
    # key.release(Key.down)
    key.press(Key.space)
    # print('jump')
    time.sleep(0.1)
    key.release(Key.space)
    # key.press(Key.down)

def show_active_win():
    # Get all opened windows
    hwnd_title = dict()
    def get_all_hwnd(hwnd,mouse):
        if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
            hwnd_title.update({hwnd:win32gui.GetWindowText(hwnd)})
    
    win32gui.EnumWindows(get_all_hwnd, 0)
    for h,t in hwnd_title.items():
        if t != "":
            print(h, t)
    

show_active_win()
startgame()
  
with mss.mss() as sct:
    # Part of the screen to capture

    monitor = {'top': 770, 'left': 220, 'width': 900, 'height': 300}

    while 'Screen capturing':
        # key.press(Key.down)
        # Get raw pixels from the screen, save it to a Numpy array
        # img = numpy.array(sct.grab(monitor))
        img = grab_screen_win32("Apex Legends", (180,240,500,300))
          
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        res1 = cv2.matchTemplate(img_gray, tree1, cv2.TM_CCOEFF_NORMED)
        res4 = cv2.matchTemplate(img_gray, tree4, cv2.TM_CCOEFF_NORMED)
        res3 = cv2.matchTemplate(img_gray, bird, cv2.TM_CCOEFF_NORMED)

        threshold = 0.65

        loc2 = numpy.where(res1 >= threshold)
        # if len(loc2[0]) > 0:
        #     ms = (loc2[1][0]+220,loc2[0][0]+770)
        #     pyautogui.moveTo(ms)

        draw = 0
        for pt in zip(*loc2[::-1]):
            if not draw:
                cv2.rectangle(img, pt, (pt[0] + tw, pt[1] + th), (0, 0, 255), 2)
                draw = 1
            if pt[0] + tw < 350:
                print("tree1")
                jump()   
                break
        
        loc2 = numpy.where(res3 >= threshold)
        for pt in zip(*loc2[::-1]):
            cv2.rectangle(img, pt, (pt[0] + nw, pt[1] + nh), (0, 0, 255), 2)
            print("bird {0},{1}".format(pt[0], pt[1]))
            if pt[1] < 150 and pt[0] + nw < 350:
                key.press(Key.down)
                # print('jump')
                time.sleep(0.5)
                key.release(Key.down)
            if pt[1] > 150 and pt[0] + nw < 350:
                jump()
            break

        loc5 = numpy.where(res4 >= threshold)
        draw = 0
        for pt in zip(*loc5[::-1]):
            if not draw:
                cv2.rectangle(img, pt, (pt[0] + tw4, pt[1] + th4), (0, 0, 255), 2)
                draw = 1
            if pt[0] + tw4 < 350:
                print("tree2")
                jump()
                break

        # Display the picture
        cv2.imshow('OpenCV/Numpy normal', img)

        # Press "q" to quit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break