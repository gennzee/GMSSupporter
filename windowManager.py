import win32gui
from PIL import ImageGrab

def move_window(hwnd, x, y, n_width, n_height, b_repaint):
    win32gui.MoveWindow(hwnd, x - 9, y - 32, n_width, n_height, b_repaint)

def move_window_top_left():
    #hwnd = win32gui.FindWindow(None, "Ristonia - A Better 64-bit Mushroom Game")
    hwnd = win32gui.FindWindow(None, "Maplestory")
    rect = win32gui.GetWindowRect(hwnd)
    x = rect[0]
    y = rect[1]
    w = rect[2] - x
    h = rect[3] - y
    print("\tWindow   : %s" % win32gui.GetWindowText(hwnd))
    print("\tLocation : (%d, %d)" % (x, y))
    print("\tSize     : (%d, %d)" % (w, h))
    move_window(hwnd, 0, 0, w, h, True)
    bbox = win32gui.GetWindowRect(hwnd)
    img = ImageGrab.grab(bbox)

if __name__ == '__main__':
    move_window_top_left()