import time
import win32gui, win32ui, win32con, win32api
import numpy as np
from PIL import ImageGrab
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import *
import sys
import cv2

def grab_screen_pil():
    img = ImageGrab.grab(bbox=(0, 0, 2736, 1824))
    img = np.array(img.getdata(), np.uint8).reshape(img.size[1], img.size[0], 3)

def grab_screen_win32(window=None, rect=None):
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
    img = np.frombuffer(saveBitMap.GetBitmapBits(True), dtype="uint8")
    img.shape = (h,w,4)
    img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
    # save img
    # saveBitMap.SaveBitmapFile(saveDC, "screenshot.jpg")

    # Free win
    win32gui.DeleteObject(saveBitMap.GetHandle())
    mfcDC.DeleteDC()
    saveDC.DeleteDC()

    return img

def grab_screen_PyQt(win=None):
    hwnd = win32gui.FindWindow(None, win)
    app = QApplication(sys.argv)
    screen = QApplication.primaryScreen()
    img = screen.grabWindow(hwnd).toImage()
    # img.save("screenshot.jpg")

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

def main():
    # time_tag = time.time()
    # for i in range(10):
    #     grab_screen_pil()
    # print(f'pil time: {time.time()-time_tag} FPS: {10/(time.time()-time_tag)}')

    # time_tag = time.time()
    # for i in range(10):
    #     grab_screen_win32()
    # print(f'win32 time: {time.time()-time_tag} FPS: {10/(time.time()-time_tag)}')

    # time_tag = time.time()
    # for i in range(10):
    #     grab_screen_PyQt()
    # print(f'PyQt time: {time.time()-time_tag} FPS: {10/(time.time()-time_tag)}')

    show_active_win()
    # img = grab_screen_win32("T-Rex Game. - Google Chrome")

if __name__ == '__main__':
    main()
