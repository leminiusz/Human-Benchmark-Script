import pyautogui
import time
import keyboard
import random
import win32api, win32con

def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

#for me position is (456,374) CHANGE TO YOUR NEEDS
x,y = 456,374

while not keyboard.is_pressed('q'):
    current_color= pyautogui.pixel(x, y)
    if current_color==(43,135,209):
        click(x,y)
        time.sleep(0.1)
        while current_color==(206,58,34):
            if keyboard.is_pressed('q'):    
                break
        time.sleep(0.5)
    elif current_color==(75,219,106):
            click(x,y)
            time.sleep(0.5)
        
    